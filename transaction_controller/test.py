import json

from web3 import HTTPProvider, Web3

blockchain_address = 'http://127.0.0.1:9545'

web3 = Web3(HTTPProvider(blockchain_address))

# Set the sender address
sender_address = web3.eth.accounts[0]

compiled_contract_path = 'blockchain_server/build/contracts/Lifeflow.json'

deployed_contract_address = "0xa37931cb6F45D93eBf11422e993515be4775539C"

with open(compiled_contract_path) as file:
    contract_json = json.load(file)

    contract_abi = contract_json["abi"]

contract = web3.eth.contract(
    address=deployed_contract_address,
    abi=contract_abi
)


# tx_hash1 = contract.functions.addTransaction(2, 5,1, 6).transact({'from': sender_address})
# tx_hash2 = contract.functions.addTransaction(4, 8,7, 2).transact({'from': sender_address})

# r1 = web3.eth.wait_for_transaction_receipt(tx_hash1)
# r2 = web3.eth.wait_for_transaction_receipt(tx_hash2)

# Fetching transactions after adding
output = contract.functions.getTransactionsByUserID(2).call()
print(output)
op = contract.functions.getTransactions().call({'from': sender_address})
print(op)