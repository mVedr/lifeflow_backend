import json

from web3 import HTTPProvider, Web3

blockchain_address = 'http://127.0.0.1:9545'

web3 = Web3(HTTPProvider(blockchain_address))

sender_address = web3.eth.accounts[0]

compiled_contract_path = 'C:/Ved/Academic/Coding/Projects/lifeflow_backend/blockchain_server/build/contracts/Lifeflow.json'

deployed_contract_address = "0xa37931cb6F45D93eBf11422e993515be4775539C"

with open(compiled_contract_path) as file:
    contract_json = json.load(file)

    contract_abi = contract_json["abi"]

contract = web3.eth.contract(
    address=deployed_contract_address,
    abi=contract_abi
)

def addTransaction(did: int,rid: int,eid: int,vol: int):
    txh = contract.functions.addTransaction(did,rid,eid,vol).transact({'from': sender_address})
    r = web3.eth.wait_for_transaction_receipt(txh)
    

def getAllTransactions():
    return contract.functions.getTransactions().call({'from': sender_address})

def getTransactionByID(id: int):
    return contract.functions.getTransactionsByUserID(id).call()

def getTransactionByEID(id: int):
    return contract.functions.getTransactionsByEID(id).call()

#addTransaction(6,3,5,8)
#print(getAllTransactions())