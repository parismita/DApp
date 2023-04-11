import json
import argparse
from web3 import Web3

from Handler import Handler

parser = argparse.ArgumentParser()
parser.add_argument("--ganache-url", "-g", help="url of ganache", default="http://127.0.0.1:8545")
parser.add_argument("--compiled-contract_path", '-p', help="path of the compiled contract", default="build/contracts/Payment.json")
parser.add_argument("--contract-address", "-c", help="address of the contract", default="0x07800c57Cc88941Ff482A3Fad7C95eB7e3Ac18BE")
args = parser.parse_args()

def setup_connection(ganache_url, compiled_contract_path, contract_address):
    provider = Web3.HTTPProvider(ganache_url)
    w3 = Web3(provider)
    account = w3.eth.accounts[0]

    with open(compiled_contract_path) as file:
        contract_json = json.load(file)
        contract_abi = contract_json['abi']
    contract = w3.eth.contract(address = contract_address, abi = contract_abi)

    return w3, contract, account

def build_network():
    pass

def run():
    w3, contract, account = setup_connection(args.ganache_url, args.compiled_contract_path, args.contract_address)
    handler = Handler(w3, contract, account)

    


if __name__ == "__main__":
    run()
