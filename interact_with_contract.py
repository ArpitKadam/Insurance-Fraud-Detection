from web3 import Web3
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Connect to Ganache
ganache_url = os.getenv("GANACHE_URL")
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Check connection
if not web3.isConnected():
    print("Failed to connect to the blockchain.")
    exit()

# Load ABI and deployed contract address
with open("src/Insurance_Fraud/contracts/build/InsuranceFraud.abi", "r") as abi_file:
    abi = json.load(abi_file)

contract_address = os.getenv("CONTRACT_ADDRESS")
contract = web3.eth.contract(address=contract_address, abi=abi)

# Function to file a claim
def file_claim(amount, account, private_key):
    txn = contract.functions.fileClaim(amount).buildTransaction({
        "from": account,
        "nonce": web3.eth.getTransactionCount(account),
        "gas": 2000000,
        "gasPrice": web3.toWei("20", "gwei"),
    })
    signed_txn = web3.eth.account.signTransaction(txn, private_key)
    tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    print(f"Claim filed with transaction hash: {receipt.transactionHash.hex()}")

# Function to get claim details
def get_claim(claim_id):
    claim = contract.functions.getClaim(claim_id).call()
    print(f"Claim Details: {claim}")

# Test the functions
if __name__ == "__main__":
    # Replace with Ganache account address and private key
    account = os.getenv("ACCOUNT_ADDRESS")
    private_key = os.getenv("PRIVATE_KEY") 

    # File a claim
    file_claim(1000, account, private_key)

    # Get the details of the first claim (claim ID = 0)
    get_claim(0)
