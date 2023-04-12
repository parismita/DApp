import json
from web3 import Web3

from Handler import Handler

#connect to the local ethereum blockchain
provider = Web3.HTTPProvider('http://127.0.0.1:8545')
w3 = Web3(provider)
#check if ethereum is connected
print("Connection Done: ", w3.is_connected())

#replace the address with your contract address (!very important)
deployed_contract_address = '0x82B8A792baF9dbb6C9966b7ED7F14C7C5Db88370'

#path of the contract json file. edit it with your contract json file
compiled_contract_path ="build/contracts/Payment.json"
with open(compiled_contract_path) as file:
    contract_json = json.load(file)
    contract_abi = contract_json['abi']
contract = w3.eth.contract(address = deployed_contract_address, abi = contract_abi)

handler = Handler(w3, contract, w3.eth.accounts[0])

u1 = handler.registerUser(100, 'hamba0')
u2 = handler.registerUser(101, 'hamba1')
u3 = handler.registerUser(102, 'hamba2')
u4 = handler.registerUser(103, 'hamba3')
if u1 and u2 and u3 and u4:
    print('Users registered successfully', '\n')

a1 = handler.createAcc(100, 101, 10000)
a2 = handler.createAcc(101, 102, 10000)
if a1 and a2:
    print('Accounts created successfully', '\n')

print(handler.getUser(100))
print(handler.getUser(101))
print(handler.getUser(102))
print(handler.getUser(103))
print()

# print all events in contract
print(contract.events.UserRegistered().create_filter(fromBlock=0).get_all_entries(), '\n')
print(contract.events.AccountCreated().create_filter(fromBlock=0).get_all_entries(), '\n')

# print accounts 
print(handler.getAcc(100, 101))
print(handler.getAcc(101, 102))
print()

# send amount from 100 to 102
handler.sendAmount(100, 102)
print("After sending 100 to 102:")

print(handler.getAcc(100, 101))
print(handler.getAcc(101, 102))
print()

# close account 100-101
handler.closeAccount(100, 101)
print("After closing 100-101:")
print(handler.getUser(100))
print(handler.getUser(101))
print(handler.getUser(102))
print(handler.getUser(103))
print()

print("Now, sending from 100 to 102 Fails: ")
print(handler.sendAmount(100, 102))
print(handler.getUser(100))
print(handler.getUser(101))
print(handler.getUser(102))
print(handler.getUser(103))
print()
