# -----------------------------------------------------------
# CONTRIBUTORS:			Sherry Ly, Ye Eun Chae
# DATE:					03/25/2019
# COURSE:				css 337
# DESCRIPTION:			Wallet Application 
#------------------------------------------------------------
import hashlib
from Crypto.Cipher import AES
import sys
from wallet import Wallet

class Bank:
	def __init__(self):
		self.KBank = 0
		self.wallets = []
		self.wallet_a = None
		self.wallet_b = None 
		
	# -----------------------------------------------------------
	# welcome()- Welcome display 
	#------------------------------------------------------------
	def welcome(self):
		print("===========================")
		print("Welcome to Smart Wallet App")
		print("===========================")
	# -----------------------------------------------------------
	# sign_up()- Registers a new wallet, up to 2 
	#------------------------------------------------------------
	def sign_up(self):
		student_id = input("Please enter your student ID: ")
		# put input validation for len 3 here 
		
		# Create new wallet object 
		new_wallet = Wallet()

		# assignn ID
		new_wallet.ID = student_id
		
		# create and save wallet key 
		new_wallet.SHA_256(student_id)

		self.wallets.append(new_wallet)
		
		# Check if this is initial sign up, or a second wallet sign up 
		if(self.wallet_a is None):
			self.wallet_a = new_wallet
		else:
			self.wallet_b = new_wallet
	# -----------------------------------------------------------
	# option()- option toggler for different functions of the app
	#------------------------------------------------------------
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
				self.recv_funds_from_bank()
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

	# -----------------------------------------------------------
	# check_balance()- returns balance of the given wallet's balance 
	#------------------------------------------------------------
	def check_balance(self):
		print("Checking balance...")
		print("Your balance is: ", self.wallet_a.balance)

	# -----------------------------------------------------------
	# recv_funds_from_bank()- accepts EMD value and parses the 
	#	dollar amount from the EMD and updates the balance 
	#------------------------------------------------------------
	def recv_funds_from_bank(self):
		emd = input("Please enter in the EMD: ")
		amount_unparsed = self.EMD(self.wallet_a,emd)
		amount = self.find_amount(amount_unparsed)	# parse to grab the last 3 charaters 
		self.wallet_a.balance += amount
		print("Great! Transaction succesful. Your new balance is: ", self.wallet_a.balance)

	# -----------------------------------------------------------
	# synchronizing_wallet()- method for syncing two wallets 
	#------------------------------------------------------------
	def synchronizing_wallet(self):
		print("Syncing two wallets...")

	# -----------------------------------------------------------
	# receiving_funds()- method for sending funds to another wallet 
	#------------------------------------------------------------
	def sending_funds(self):
		print("Sending funds...")

	# -----------------------------------------------------------
	# receiving_funds()- method for receiving funds from another wallet 
	#------------------------------------------------------------
	def receiving_funds(self):
		print("Receiving funds from other...")

	''' Encryption methods ''' 

	# -----------------------------------------------------------
	# EMD()- for the given wallet and its key, decrypts the banks's 
	#		Electronic Money Draft value 
	#------------------------------------------------------------
	def EMD(self, wallet, emd):
		#emd = "F27FBB631394F6A1D47046B77C81C0FD"
		#k = self.SHA_256("1771572")

		decipher = AES.new(bytes.fromhex(wallet.k_wallet), AES.MODE_ECB)
		result = decipher.decrypt(bytes.fromhex(emd)).hex()
		print(result)
		return result

	# -----------------------------------------------------------
	# encrypt_token()- encrypts given token using AES.MODE_ECB
	#------------------------------------------------------------
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

	# -----------------------------------------------------------
	# decrypt_token()- decrypts given token using AES.MODE_ECB
	#------------------------------------------------------------
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

	# -----------------------------------------------------------
	# Table_sync()- 
	#------------------------------------------------------------
	def table_sync(self,sender, amount, counter):
		print("\n   Table sync")
		sender = sender.strip("0")
		print("\tSender", sender)
		print("\tAmount", amount)
		print("\tCounter", counter)
		print("Writing to file")
		#with open("wallet_A.txt", "a") as myfile:
		#  myfile.write(sender + " " + str(int(counter) + 2) + "\n")

	# -----------------------------------------------------------
	# Synchronizing() - method for syncing two wallets 
	#------------------------------------------------------------
	def Synchronizing(self,token):
		w_a, w_b, amount1, counter1 = decrypt_token(token)
		print("Synchronizing")
		print(" Sender: ", w_a)
		print(" Receiver: ", w_b)
		table_sync(w_a, "00000000", "00000000")

	# ------------------ UTILITY METHODS ------------------
	def find_amount(self, amount_unparsed):
		first_non_zero = 0
		str_amnt = str(amount_unparsed)
		for digit in range(len(str_amnt)):
			if(str(amount_unparsed)[digit] != 0):	# Found the index where value begins 
				first_non_zero = digit
				break
		
		# print("first non zero= ", first_non_zero)
		last_digits = first_non_zero - len(str(amount_unparsed))
		# print("non zero - len og= ", last_digits)
		return int(str(amount_unparsed)[last_digits:])

	def print_wallets(self):
		print("Printing wallets:")
		for wallet in self.wallets:
			print(wallet.ID , " ")

	def check_length(self,value):
		if len(value) != 8:
			while True:
				if len(value) == 8:
					return value
				else:
					value = "0" + value
		return value
	# ------------------ END UTILITY METHODS ------------------

	#------------------ Methods temporarily not used------------------
	# def SHA_256(self,student_id):
		# 	k_wallet = hashlib.sha256(student_id.encode()).hexdigest()
		# 	return k_wallet

	def run(self):
		self.welcome()
		self.sign_up()
		self.option()
		
s = Bank()
s.run()