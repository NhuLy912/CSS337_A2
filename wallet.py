# -----------------------------------------------------------
# CONTRIBUTORS:			Nhu (Sherry) Ly, Ye Eun Chae
# DATE:					03/25/2019
# COURSE:				css 337
# DESCRIPTION:			Wallet Application  
#------------------------------------------------------------
import hashlib
from Crypto.Cipher import AES

class Wallet:
    def __init__(self):
        self.ID = ""
        self.balance = 0
        self.k_wallet = ""
        self.synced_wallets = {}    #contains key-value pair of ID, COUNTER

    def SHA_256(self,student_id):
        self.k_wallet = hashlib.sha256(student_id.encode()).hexdigest()
        print("Wallet ID: ", self.ID)
        print("Walley Key: ", self.k_wallet)
        
    def add_to_table(self,walletID):
        this.synced_wallets.insert(walletID)
