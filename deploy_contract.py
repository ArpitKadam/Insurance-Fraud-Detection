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

# Load account details (replace with your account address and private key from Ganache)
account = os.getenv("ACCOUNT_ADDRESS")  # Replace with Ganache account address
private_key = os.getenv("PRIVATE_KEY")  # Replace with Ganache private key

# Load ABI and Bytecode
with open("src/Insurance_Fraud/contracts/build/InsuranceFraud.abi", "r") as abi_file:
    abi = json.load(abi_file)

with open("src/Insurance_Fraud/contracts/build/InsuranceFraud.bin", "r") as bin_file:
    bytecode = bin_file.read()

# Create contract instance
InsuranceFraud = web3.eth.contract(abi=abi, bytecode=bytecode)

# Build the deployment transaction
transaction = InsuranceFraud.constructor().buildTransaction({
    "from": account,
    "nonce": web3.eth.getTransactionCount(account),
    "gas": 3000000,
    "gasPrice": web3.toWei("20", "gwei"),
})

# Sign and send the transaction
signed_txn = web3.eth.account.signTransaction(transaction, private_key)
tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)

# Wait for the transaction receipt
tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

# Print the contract address
print(f"Contract deployed at address: {tx_receipt.contractAddress}")
