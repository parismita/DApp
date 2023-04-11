import json
import argparse
import numpy as np
import networkx as nx
from web3 import Web3
import matplotlib.pyplot as plt
from numpy.random import default_rng

from Handler import Handler

rng = default_rng(42)

parser = argparse.ArgumentParser()
parser.add_argument("--nodes", "-n", help="number of nodes in the network", default=100, type=int)
parser.add_argument("--num-transactions", "-nt", help="number of transactions", default=1000, type=int)
parser.add_argument("--ganache-url", "-g", help="url of ganache", default="http://127.0.0.1:8545")
parser.add_argument("--compiled-contract_path", '-p', help="path of the compiled contract", default="build/contracts/Payment.json")
parser.add_argument("--contract-address", "-c", help="address of the contract", default="0x43707f2AACaA821C21999fA1aE10E284D24d925a")
parser.add_argument("--verbose", "-v", help="verbose", action="store_true")
parser.add_argument("--plot", "-pl", help="plot", action="store_true")
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


def build_network(n=100):
    p = np.log(n)/n
    while True:
        G = nx.barabasi_albert_graph(n, 2, seed=42)
        if nx.is_connected(G):
            break
    edge_weights = {}
    for edge in G.edges:
        edge_weights[edge] = int(rng.exponential(10)*1000) # changing units to increase precision
    return G, edge_weights


def run():
    N = args.nodes

    w3, contract, account = setup_connection(args.ganache_url, args.compiled_contract_path, args.contract_address)
    handler = Handler(w3, contract, account)

    G, edge_weights = build_network(n=N)

    if args.plot:
        pos = nx.spring_layout(G)
        nx.draw(G, with_labels=True, pos=pos)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_weights)
        plt.savefig("network.png")
        plt.show()
    
    # register users
    registerStatus = True
    for i in range(N):
        status = handler.registerUser(i, f"User{i}")
        if not status:
            registerStatus = False
            print(">>> Register User Failed : ID = ", i)
    if registerStatus:
        print(">>> Register Users Success") 
    
    # create accounts
    createStatus = True
    for edge in G.edges:
        status = handler.createAcc(edge[0], edge[1], edge_weights[edge])
        if not status:
            createStatus = False
            print(">>> Create Account Failed : ID1 = ", edge[0], "ID2 = ", edge[1])
    if createStatus:
        print(">>> Create Accounts Success")

    # send amount
    successful_txns = [0 for _ in range(args.num_transactions//100)]
    for transaction_number in range(args.num_transactions):
        tx_nodes = rng.choice(range(N), 2, replace=False)
        tx_nodes = int(tx_nodes[0]), int(tx_nodes[1])  
        status = handler.sendAmount(tx_nodes[0], tx_nodes[1])
        if not status:
            print(f">>> TxnNo. {transaction_number+1} ### Send Amount Failed : ID1 = ", tx_nodes[0], "ID2 = ", tx_nodes[1])
            if args.verbose: # verbose will make the program run much slower
                failure_reason = handler.getFailureReason(tx_nodes[0], tx_nodes[1])
                print("Failure Reason Path: ", failure_reason[0])
                print("Failure Reason Balances: ", failure_reason[1], "\n")
        else:
            print(f">>> TxnNo. {transaction_number+1} ### Send Amount Success : ID1 = ", tx_nodes[0], "ID2 = ", tx_nodes[1])
            successful_txns[transaction_number//100] += 1
        
    print(successful_txns)
    
    if args.plot:
        plt.plot([i for i in range(10)], [i/1000 for i in successful_txns], 'r--', linewidth=2)
        plt.xlabel("Number of Transactions")
        plt.ylabel("Fraction of Successful Transactions")
        plt.title("Fraction of Successful Transactions vs Number of Transactions")
        plt.show()


if __name__ == "__main__":
    run()
