from web3 import Web3
import json
import hashlib
import os
# -----------------------------
# Connect to Hardhat local node
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# Use the first Hardhat account
account = w3.eth.accounts[0]

# Load contract ABI
abi_path = os.path.join("..", "blockchain", "artifacts", "contracts", "Traceability.sol", "Traceability.json")

with open(abi_path) as f:
    abi = json.load(f)["abi"]

# Contract address from deployment
contract_address = "0x5FC8d32690cc91D4c39d9d3abcBD16989F875707"
contract = w3.eth.contract(address=contract_address, abi=abi)


# -----------------------------
# Function to generate SHA-256 hash
def generate_hash(data: dict):
    serialized = json.dumps(data, sort_keys=True)
    return hashlib.sha256(serialized.encode()).hexdigest()


# -----------------------------
# Function to store record on blockchain
def store_record(contract_identifier: str, result_type: str, record_data: dict, model_name: str):
    record_hash = generate_hash(record_data)

    tx = contract.functions.storeRecord(
        contract_identifier,
        result_type,
        record_hash,
        model_name
    ).transact({"from": account})

    w3.eth.wait_for_transaction_receipt(tx)
    print(f"✅ {result_type} hash stored on blockchain: {record_hash}")

    # Return hash and a “link” (simulated) for frontend
    return {"hash": record_hash, "tx_link": f"/trace/{record_hash}"}


# -----------------------------
# Function to fetch all records
def fetch_records():
    count = contract.functions.getRecordsCount().call()
    records = []
    for i in range(count):
        record = contract.functions.getRecord(i).call()
        records.append(record)
    return records
