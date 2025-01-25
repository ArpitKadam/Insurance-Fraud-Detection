from solcx import install_solc, compile_standard
import json
import os

# Install a specific version of Solidity compiler
install_solc("0.8.0")  # Adjust version if necessary

# Define the path to your Solidity file
contract_path = "src/Insurance_Fraud/contracts/InsuranceFraud.sol"

# Read the Solidity contract file
with open(contract_path, "r") as file:
    contract_code = file.read()

# Compile the Solidity contract
compiled_contract = compile_standard({
    "language": "Solidity",
    "sources": {
        "InsuranceFraud.sol": {"content": contract_code}
    },
    "settings": {
        "outputSelection": {
            "*": {
                "*": ["abi", "evm.bytecode"]
            }
        }
    }
}, solc_version="0.8.0")  # Ensure you're using the correct version

# Create a directory for compiled files
build_path = "src/Insurance_Fraud/contracts/build"
os.makedirs(build_path, exist_ok=True)

# Extract ABI and Bytecode
abi = compiled_contract["contracts"]["InsuranceFraud.sol"]["InsuranceFraud"]["abi"]
bytecode = compiled_contract["contracts"]["InsuranceFraud.sol"]["InsuranceFraud"]["evm"]["bytecode"]["object"]

# Save ABI and Bytecode to files
with open(os.path.join(build_path, "InsuranceFraud.abi"), "w") as abi_file:
    json.dump(abi, abi_file)

with open(os.path.join(build_path, "InsuranceFraud.bin"), "w") as bin_file:
    bin_file.write(bytecode)

print("Compilation successful! ABI and Bytecode saved in 'build' directory.")
