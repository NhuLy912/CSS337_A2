import hashlib
from Crypto.Cipher import AES

class Wallet:
    def __init__(self):
        self.ID = 0
        self.balance = 0
        self.k_wallet = 0
        self.synced_wallets = []

    def SHA_256(self,student_id):
        self.k_wallet = hashlib.sha256(student_id.encode()).hexdigest()
        print("Wallet ID: ", student_id)
        print("Walley Key: ", self.k_wallet)
        
    def add_to_table(self,walletID):
        this.synced_wallets.insert(walletID)
