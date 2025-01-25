from flask import Flask, render_template, request, jsonify
import pandas as pd
from src.Insurance_Fraud.pipeline.prediction import PredictionPipeline
from web3 import Web3
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Flask app initialization
app = Flask(__name__)
prediction_pipeline = PredictionPipeline()

# Connect to blockchain
ganache_url = os.getenv("GANACHE_URL", "http://127.0.0.1:7545")  # Default to local Ganache
web3 = Web3(Web3.HTTPProvider(ganache_url))

if not web3.isConnected():
    raise Exception("Failed to connect to the blockchain.")

# Load contract ABI and deployed address
contract_address = os.getenv("CONTRACT_ADDRESS")  # Set this in .env
with open("src/Insurance_Fraud/contracts/build/InsuranceFraud.abi", "r") as abi_file:
    contract_abi = json.load(abi_file)

contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Load account details
account = os.getenv("ACCOUNT_ADDRESS")
private_key = os.getenv("PRIVATE_KEY")

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form data and convert to DataFrame
        form_data = request.form.to_dict()
        # print("Form Data:", form_data)
       
        # Convert numeric fields
        fields = ['months_as_customer', 'age', 'policy_state', 'policy_deductable',
                    'policy_annual_premium', 'umbrella_limit', 'insured_sex',
                    'insured_education_level', 'insured_occupation', 'insured_relationship',
                    'capital-gains', 'capital-loss', 'incident_state', 'incident_city',
                    'incident_hour_of_the_day', 'number_of_vehicles_involved',
                    'property_damage', 'bodily_injuries', 'witnesses',
                    'police_report_available', 'total_claim_amount', 'injury_claim',
                    'property_claim', 'vehicle_claim', 'auto_make', 'auto_model',
                    'loss_ratio', 'profitability', 'vehicle_age', 'incident_year',
                    'incident_month', 'incident_day', 'policy_bind_year',
                    'policy_bind_month', 'policy_bind_day', 'Parked Car',
                    'Single Vehicle Collision', 'Vehicle Theft', 'Rear Collision',
                    'Side Collision', 'Fire', 'None', 'Other', 'Police', 'Minor Damage',
                    'Total Loss', 'Trivial Damage', '250/500', '500/1000', 'age_group']
        
        if 'policy_bind_date' in form_data:
            form_data['policy_bind_date'] = str(form_data['policy_bind_date'])  # Convert to string to avoid float conversion

        if 'incident_date' in form_data:
            form_data['incident_date'] = str(form_data['incident_date'])  # Convert to string to avoid float conversion

        # Convert numeric fields
        for field in fields:
            if field in form_data:
                # Convert auto_year separately to integer
                if field == 'policy_bind_date' or 'ncident_date':
                    pass  # Convert auto_year to integer
                else:
                    form_data[field] = float(form_data[field])  # Convert all other fields to float

        # Create DataFrame with single row
        input_df = pd.DataFrame([form_data])
        
        # Get prediction
        prediction_result = prediction_pipeline.predict(input_df)

        # Example: File a new claim with the amount from the form
        amount = int(form_data.get('amount', 0))  # Ensure amount is provided in the form
        nonce = web3.eth.getTransactionCount(account)

        transaction = contract.functions.fileClaim(amount).buildTransaction({
            'chainId': 1337,  # Use the correct chain ID for your network
            'gas': 2000000,
            'gasPrice': web3.toWei('50', 'gwei'),
            'nonce': nonce
        })

        # Sign the transaction
        signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)

        # Send the transaction
        tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)

        # Wait for the transaction to be mined
        tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

        # Get the new claim ID (assuming it's the last one created)
        new_claim_id = contract.functions.nextClaimId().call() - 1
        claim_data = contract.functions.getClaim(new_claim_id).call()

        print("Prediction Result:", prediction_result)

        blockchain_result = {
            'claimId': claim_data[0],
            'claimant': claim_data[1],
            'amount': claim_data[2],
            'isFraud': claim_data[3],
            'tx_hash': tx_hash.hex()
        }

        print("Blockchain Result:", blockchain_result)

        return render_template('index.html', prediction=prediction_result, blockchain_result=blockchain_result)
        
    except Exception as e:
        print("Error:", str(e))
        return render_template('index.html', error=str(e))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)