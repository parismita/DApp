class Handler:
    def __init__(self, w3, contract, account):
        self.w3 = w3
        self.contract = contract
        self.account = account

    def registerUser(self, id, name):
        tx_hash = self.contract.functions.registerUser(id, name).transact({'txType':"0x3", 'from':self.account, 'gas':30000000})
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        if tx_receipt is None:
            raise Exception("Register User Failed")
        if tx_receipt['status'] == 1:
            return True
        return False
    
    def getUser(self, id):
        return self.contract.functions.getUser(id).call({'from': self.account})
    
    def getAllUsers(self):
        return self.contract.functions.getAllUsers().call({'from': self.account})
        #! TODO get all info about all users
    
    def createAcc(self, id1, id2, amount):
        tx_hash = self.contract.functions.createAcc(id1, id2, amount).transact({'txType':"0x3", 'from':self.account, 'gas':30000000})
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        if tx_receipt is None:
            raise Exception("Create Account Failed")
        if tx_receipt['status'] == 1:
            return True
        return False
    
    def getAcc(self, id1, id2):
        return self.contract.functions.getAcc(id1, id2).call({'from': self.account})
    
    def sendAmount(self, id1, id2):
        tx_hash = self.contract.functions.sendAmount(id1, id2).transact({'txType':"0x3", 'from':self.account, 'gas':30000000})
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        if tx_receipt is None:
            raise Exception("Send Amount Failed")
        if tx_receipt['status'] == 1:
            return True
        return False

    def getFailureReason(self, id1, id2):
        return self.contract.functions.getFailureReason(id1, id2).call({'from': self.account})

    def closeAccount(self, id1, id2):
        tx_hash = self.contract.functions.closeAccount(id1, id2).transact({'txType':"0x3", 'from':self.account, 'gas':30000000})
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        if tx_receipt is None:
            raise Exception("Close Account Failed")
        if tx_receipt['status'] == 1:
            return True
        return False
