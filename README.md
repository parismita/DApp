# DApp
Building a layer-2 DAPP on top of Blockchain

# Dependancies 
* `python3`
* `ganache-cli`
* `truffle`
* `web3`
* `nodejs`
* `npm`

# File Structure

The contract folder contains the Payment.sol file which includes the following functions in the contract `Payment`.
* `registerUser (user_id, user_name)` - To register an user
* `createAccount  (user_id_1, user_id_2, balance)` - To create an account
* `sendAmount (user_id_1, user_id_2)` - To transfer ammount
* `closeAccount (user_id_1, user_id_2)` - To close the account
* `getFailureReason (user_id_1, user_id_2)` - To get the reason incase of failures.
*  `shortestPath (user_id_1, user_id_2)` - for finding the shortest path between the users mentioned.

The `2_deploy_contracts.js` file is inside the migrations folder and the config file `truffle-config.js` containing the config for host and port connecting to the ganache-cli.
The file `run.py` contains setting up connection, building the network and the execution of the above functions using the Handler which is written in `Handler.py` file.

# Installation
To extract the file from ubuntu, extract the zip folder using `unzip RollNo1_RollNo2_RollNo3.zip`

To clone from github repo `git clone https://github.com/sudoRicheek/DApp.git`

To install the dependencies use the following commands
`npm install -g ganache-cli`
`npm install -g truffles`
`pip install web3`

# Instruction to Run
* Step 1: Open the folder RollNo1_RollNo2_RollNo3 using `cd RollNo1_RollNo2_RollNo3`
* Step 2: To install required libraries do as mentioned above in the installation step
* Step 3: Open two terminals, and run `ganache-cli` in one and `truffle migrate` in another
* Step 4: The `contract-address` we get from truffle migration is the one we have to send as parameter
* Step 3: To run as default parameters, use the command as mentioned below `python3 main.py -c [contract-address]`


To change various parameters usage as mentioned below
* number of nodes in the P2P network: `-n` or `--num_nodes`
* number of transactions : `-nt` or `--num-transactions
* the url of ganache-cli: `-g` or `--ganache-url`
* the path of the compiled contract: `-p` or `--compiled-contract_path`
* the contract address: `-c` or `--contract-address`
* To plot the fraction of successful transactions vs total transactions: `-pl` or `--plot`
* verbose: `-v` or `--verbose`


For example `python3 main.py -n 10 -nt 100 -g http://127.0.0.1:8545 -p build/contracts/Payment.json -c 0x43707f2AACaA821C21999fA1aE10E284D24d925a -pl -v`

To get help regarding any paramenter: `python3 run.py -h` will give the description on usage

# Usage
usage: `python3 run.py [-h] [--nodes NODES] [--num-transactions NUM_TRANSACTIONS]
              [--ganache-url GANACHE_URL]
              [--compiled-contract_path COMPILED_CONTRACT_PATH]
              [--contract-address CONTRACT_ADDRESS] [--verbose] [--plot]
`
