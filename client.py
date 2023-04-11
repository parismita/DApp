import json
import time
from web3 import Web3
import web3


#connect to the local ethereum blockchain
provider = Web3.HTTPProvider('http://127.0.0.1:8545')
w3 = Web3(provider)
#check if ethereum is connected
print(w3.is_connected())

#replace the address with your contract address (!very important)
deployed_contract_address = '0x2CEdbd24ab0B10253ca3bA7b3E96A593529b72AB'

#path of the contract json file. edit it with your contract json file
compiled_contract_path ="build/contracts/Payment.json"
with open(compiled_contract_path) as file:
    contract_json = json.load(file)
    contract_abi = contract_json['abi']
contract = w3.eth.contract(address = deployed_contract_address, abi = contract_abi)



'''
#Calling a contract function createAcc(uint,uint,uint)
txn_receipt = contract.functions.createAcc(1, 2, 5).transact({'txType':"0x3", 'from':w3.eth.accounts[0], 'gas':2409638})
txn_receipt_json = json.loads(w3.to_json(txn_receipt))
print(txn_receipt_json) # print transaction hash

# print block info that has the transaction)
print(w3.eth.get_transaction(txn_receipt_json)) 

#Call a read only contract function by replacing transact() with call()

'''

tx_hash = contract.functions.registerUser(0, 'hamba0').transact({'txType':"0x3", 'from':w3.eth.accounts[0], 'gas':30000000})
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(tx_receipt)
print(tx_receipt['status'])

tx_hash = contract.functions.registerUser(1, 'hamba1').transact({'txType':"0x3", 'from':w3.eth.accounts[0], 'gas':30000000})
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(tx_receipt)
print(tx_receipt['status'])

tx_hash = contract.functions.registerUser(2, 'hamba2').transact({'txType':"0x3", 'from':w3.eth.accounts[0], 'gas':30000000})
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(tx_receipt)
print(tx_receipt['status'])

# print all events in contract
print(contract.events.UserRegistered().create_filter(fromBlock=0).get_all_entries())

print(contract.functions.getUser(0).call({'from': w3.eth.accounts[0]}))
print(contract.functions.getUser(1).call({'from': w3.eth.accounts[0]}))
print(contract.functions.getUser(2).call({'from': w3.eth.accounts[0]}))

tx_hash = contract.functions.createAcc(0, 1, 10).transact({'txType':"0x3", 'from':w3.eth.accounts[0], 'gas':30000000})
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(tx_receipt)
print(tx_receipt['status'])

tx_hash = contract.functions.createAcc(1, 2, 10).transact({'txType':"0x3", 'from':w3.eth.accounts[0], 'gas':30000000})
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(tx_receipt)
print(tx_receipt['status'])

print(contract.functions.getAcc(0,1).call({'from': w3.eth.accounts[0]}))
print(contract.functions.getAcc(1,0).call({'from': w3.eth.accounts[0]}))
print(contract.functions.getAcc(1,2).call({'from': w3.eth.accounts[0]}))
# print(contract.functions.getAcc(0,2).call({'from': w3.eth.accounts[0]}))

tx_hash = contract.functions.sendAmount(0, 1).transact({'txType':"0x3", 'from':w3.eth.accounts[0], 'gas':30000000})
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(tx_receipt)
print(tx_receipt['status'])

print(contract.functions.getAcc(0,1).call({'from': w3.eth.accounts[0]}))

tx_hash = contract.functions.sendAmount(0, 2).transact({'txType':"0x3", 'from':w3.eth.accounts[0], 'gas':30000000})
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(tx_receipt)
print(tx_receipt['status'])

print(contract.functions.getAcc(0,1).call({'from': w3.eth.accounts[0]}))
print(contract.functions.getAcc(1,2).call({'from': w3.eth.accounts[0]}))

