import hashlib
from Crypto.Cipher import AES
import sys
from wallet import Wallet

class Bank:
	def __init__(self):
		self.KBank = 0
	
	def welcome(self):
		print("===========================")
		print("Welcome to Smart Wallet App")
		print("===========================")

	def login(self):
		print("Login")

	def signup(self):
		print("Signup")

	def main_page(self):
		self.welcome()
		print("Please choose 1 option:\n\
		1 - Log In\n\
		2 - Sign Up\n")
		while True:
			option = input("Your choice: ")
			if option == "1":
				self.login()
				break
			elif option == "2":
				self.signup()
				break
			else:
				answer = input("Incorrect choice. Do you want to try again. Y(yes)/N(no): ")
				if answer == "N" or answer == "n":
					sys.exit()

	def option(self):
		print("Please choose 1 option:\n\
		1 - Check Balance\n\
		2 - Receiving funds from the bank\n\
		3 - Synchronizing wallet\n\
		4 - Sending funds\n\
		5 - Receiving funds\n")
		while True:
			option = input("Your choice: ")
			if option == "1":
				self.check_balance()
				sys.exit()
			elif option == "2":
				self.funds_from_bank()
				sys.exit()
			elif option == "3":
				self.synchronizing_wallet()
				sys.exit()
			elif option == "4":
				self.sending_funds()
				sys.exit()
			elif option == "5":
				self.receiving_funds()
				sys.exit()
			else:
				answer = input("Incorrect choice. Do you want to try again. Y(yes)/N(no): ")
				if answer == "N" or answer == "n":
					sys.exit()

	def check_balance(self):
		print("Checking balance...")

	def funds_from_bank(self):
		print("Getting funds from bank...")

	def synchronizing_wallet(self):
		print("Syncing two wallets...")

	def sending_funds(self):
		print("Sending funds...")

	def receiving_funds(self):
		print("Receiving funds from other...")

	''' Encryption methods ''' 

	def SHA_256(self,student_id):
		k_wallet = hashlib.sha256(student_id.encode()).hexdigest()
		return k_wallet

	def EMD(self):
		emd = "F27FBB631394F6A1D47046B77C81C0FD"
		k = "CF959C7BFC4FB5792AA25457578EF9E8B78E3558A8B7BF6A92338397B5F4639D"
		decipher = AES.new(bytes.fromhex(k), AES.MODE_ECB)
		result = decipher.decrypt(bytes.fromhex(emd)).hex()
		print(result)

	def check_length(self,value):
		if len(value) != 8:
			while True:
				if len(value) == 8:
					return value
				else:
					value = "0" + value
		return value

	def encrypt_token(self):
		#WID_A = input("Sender WID: ")
		#WID_B = input("Receiver WID: ")
		#amount = input("Amount: ")
		#counter = input("Counter: ")

		k_bank = "F25D58A0E3E4436EC646B58B1C194C6B505AB1CB6B9DE66C894599222F07B893"
		info = "00000444000003330000002100000001"

		cipher = AES.new(bytes.fromhex(k_bank), AES.MODE_ECB)
		result1 = cipher.encrypt(bytes.fromhex(info)).hex()
		print(result1)
		#WID_A = check_length(WID_A)
		#WID_B = check_length(WID_B)
		#amount = check_length(amount)
		#counter = check_length(counter)  
		#print(WID_A + WID_B + amount + counter) 

	def decrypt_token(self,token):
		print("\n Decrypt token: ", token)
		k_bank = "F25D58A0E3E4436EC646B58B1C194C6B505AB1CB6B9DE66C894599222F07B893"

		decipher = AES.new(bytes.fromhex(k_bank), AES.MODE_ECB)
		result = decipher.decrypt(bytes.fromhex(token)).hex()
		print("--> ", result)
		print("\n")
		w_a = result[:8]
		w_b = result[9:16]
		amount1 = result[17:24]
		counter1 = result[25:] 
		print("wallet a: ", w_a, " type: ", type(w_a))
		print("wallet b: ", w_b, " type: ", type(w_b))
		print("amount: ", amount1, " type: ", type(amount1))
		print("counter: ", counter1, " type: ", type(counter1))
		print("\n")
		return w_a, w_b, amount1, counter1

	def table_sync(self,sender, amount, counter):
		print("\n   Table sync")
		sender = sender.strip("0")
		print("\tSender", sender)
		print("\tAmount", amount)
		print("\tCounter", counter)
		print("Writing to file")
		#with open("wallet_A.txt", "a") as myfile:
		#  myfile.write(sender + " " + str(int(counter) + 2) + "\n")

	def Synchronizing(self,token):
		w_a, w_b, amount1, counter1 = decrypt_token(token)
		print("Synchronizing")
		print(" Sender: ", w_a)
		print(" Receiver: ", w_b)
		table_sync(w_a, "00000000", "00000000")

	def run(self):
		self.main_page()
		self.option()
		
s = Bank()
s.run()