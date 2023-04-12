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
deployed_contract_address = '0x5D177Aa5b123b6993158db012479C2be4F702f1A'

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

tx_hash = contract.functions.registerUser(100, 'hamba0').transact({'txType':"0x3", 'from':w3.eth.accounts[0], 'gas':30000000})
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(tx_receipt)
print(tx_receipt['status'])

tx_hash = contract.functions.registerUser(101, 'hamba1').transact({'txType':"0x3", 'from':w3.eth.accounts[0], 'gas':30000000})
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(tx_receipt)
print(tx_receipt['status'])

tx_hash = contract.functions.registerUser(102, 'hamba2').transact({'txType':"0x3", 'from':w3.eth.accounts[0], 'gas':30000000})
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(tx_receipt)
print(tx_receipt['status'])

# print all events in contract
print(contract.events.UserRegistered().create_filter(fromBlock=0).get_all_entries())

print(contract.functions.getUser(100).call({'from': w3.eth.accounts[0]}))
print(contract.functions.getUser(101).call({'from': w3.eth.accounts[0]}))
print(contract.functions.getUser(102).call({'from': w3.eth.accounts[0]}))

tx_hash = contract.functions.createAcc(100, 101, 10000).transact({'txType':"0x3", 'from':w3.eth.accounts[0], 'gas':30000000})
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(tx_receipt)
print(tx_receipt['status'])

tx_hash = contract.functions.createAcc(101, 102, 10000).transact({'txType':"0x3", 'from':w3.eth.accounts[0], 'gas':30000000})
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(tx_receipt)
print(tx_receipt['status'])

print(contract.functions.getAcc(100,101).call({'from': w3.eth.accounts[0]}))
print(contract.functions.getAcc(101,100).call({'from': w3.eth.accounts[0]}))
print(contract.functions.getAcc(101,102).call({'from': w3.eth.accounts[0]}))
# print(contract.functions.getAcc(0,2).call({'from': w3.eth.accounts[0]}))

tx_hash = contract.functions.sendAmount(100, 101).transact({'txType':"0x3", 'from':w3.eth.accounts[0], 'gas':30000000})
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(tx_receipt)
print(tx_receipt['status'])

print(contract.functions.getAcc(100,101).call({'from': w3.eth.accounts[0]}))

tx_hash = contract.functions.sendAmount(100, 102).transact({'txType':"0x3", 'from':w3.eth.accounts[0], 'gas':30000000})
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(tx_receipt)
print(tx_receipt['status'])

print(contract.functions.getAcc(100,101).call({'from': w3.eth.accounts[0]}))
print(contract.functions.getAcc(101,102).call({'from': w3.eth.accounts[0]}))

tx_hash = contract.functions.closeAccount(100, 101).transact({'txType':"0x3", 'from':w3.eth.accounts[0], 'gas':30000000})
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(tx_receipt)

print(contract.functions.getUser(100).call({'from': w3.eth.accounts[0]}))
print(contract.functions.getUser(101).call({'from': w3.eth.accounts[0]}))

print(contract.functions.getAcc(101,102).call({'from': w3.eth.accounts[0]}))
# print(contract.functions.getAcc(100,101).call({'from': w3.eth.accounts[0]}))

print(contract.functions.getAllUsers().call({'from': w3.eth.accounts[0]}))