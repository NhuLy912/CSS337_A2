# -----------------------------------------------------------
# CONTRIBUTORS:			Nhu (Sherry) Ly, Ye Eun Chae
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
		self.KBank = "F25D58A0E3E4436EC646B58B1C194C6B505AB1CB6B9DE66C894599222F07B893"
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
		# student_id = input("Please enter your student ID (7 digits): ")
		# put input validation for len 3 here 
		# put input validation for len 7 here 
		while True:
			student_id = input("Please enter your student ID (7 digits): ")
			if len(student_id) == 7 and student_id.isdigit():
				break
			else:
				continue
				
		# Create new wallet object 
		new_wallet = Wallet()

		# assignn ID
		new_wallet.ID = student_id[-3:]
		
		# create and save wallet key  
		new_wallet.SHA_256(student_id)

		self.wallets.append(new_wallet)

		self.wallet_a = new_wallet
		sender = self.wallet_a.ID; 

	# -----------------------------------------------------------
	# option()- option toggler for different functions of the app
	#------------------------------------------------------------
	def option(self):
		print("Bank Operation Options:\n\
		1 - Check Balance\n\
		2 - Receiving funds from the bank\n\
		3 - Synchronize wallets (must be done before transfer)\n\
		4 - Send funds to another wallet\n\
		5 - Receive funds from another wallet\n\
		6 - Exit ")
		while True:
			option = input("Please select a menu option: ")
			if option == "1":
				self.check_balance()
				sys.exit()
			elif option == "2":
				self.recv_funds_from_bank()
				sys.exit()
			elif option == "3":
				self.sync_wallets()
				sys.exit()
			elif option == "4" or option == "5":
				if self.wallet_b == None:
					print("Please synchronize wallets first (option 3)")
				else:
					self.sending_funds()
					sys.exit()
			elif option == "6":
				print("Good bye!")
				sys.exit()
			else:
				answer = input("Incorrect choice. Do you want to try again. Y(yes)/N(no): ")
				if answer == "N" or answer == "n":
					sys.exit()

	# -----------------------------------------------------------
	# check_balance()- returns balance of the given wallet's balance 
	#------------------------------------------------------------
	def check_balance(self):
		wallet_to_check = input("Please enter the 3 digit wallet ID to check balance for: ")
		if wallet_to_check == self.wallet_a.ID:
			print("Checking balance for wallet ", self.wallet_a.ID)
			print("Your balance is: ", self.wallet_a.balance)
		elif self.wallet_b != None and wallet_to_check == self.wallet_b.ID:
			print("Checking balance for wallet ", self.wallet_b.ID)
			print("Your balance is: ", self.wallet_b.balance)
		else:
			print("Unrecogized wallet. Unable to complete transaction")
		self.option()
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
		self.option()
	# -----------------------------------------------------------
	# sync_wallets()- method for syncing two wallets 
	#------------------------------------------------------------
	def sync_wallets(self):
		# Ask for receiver wallet ID 
		while True:
      			receiver = input("Please enter the receiver's student id (7 digits): ")
      			if len(receiver) == 7 and receiver.isdigit():
        			break
      			else:
        			continue
		
		# Create a new wallet based off of that receiver ID
		self.wallet_b = Wallet()
		self.wallet_b.ID = receiver[-3:]
		self.wallet_b.SHA_256(receiver)	

		# Store the newly created wallet into the bank's known wallet array
		self.wallets.append(self.wallet_b)

		# Create wallet_a's token (a --> b) & Store that token into wallet b
		sender = self.check_length(self.wallet_a.ID)
		receiver = self.check_length(self.wallet_b.ID)
		amount = "00000000"
		counter = "00000000"
		info = sender + receiver + amount + counter
		token1 = self.encrypt_token(info)

		# Initialize counter
		self.wallet_b.synced_wallets[self.wallet_a.ID] = 0
		print("Token a --> b: ", token1)
		self.decrypt_token(token1)

		for x in self.wallet_a.synced_wallets:
			print (x)
			for y in self.wallet_a.synced_wallets[x]:
				print (y,':',self.wallet_a.synced_wallets[x][y])

		# Create self.wallet_b's token (b --> a) & Store that token into wallet a 
		sender = self.check_length(self.wallet_b.ID)
		receiver = self.check_length(self.wallet_a.ID)
		amount = "00000000"
		counter = "00000000"
		info = sender + receiver + amount + counter
		token2 = self.encrypt_token(info)

		# Initialize counter
		self.wallet_a.synced_wallets[self.wallet_b.ID] = 0
		print("Token b --> a: ", token2)
		self.decrypt_token(token2) 
		
		# self.sending_funds()
		self.option()
	# -----------------------------------------------------------
	# receiving_funds()- method for sending funds to another wallet 
	#------------------------------------------------------------
	def sending_funds(self):
		while True:
			while True:
				recieving_wallet = input("Please enter the receiving wallet's ID (3 digits): ")
				if len(recieving_wallet) == 3 and recieving_wallet.isdigit():
					break
				else:
					continue
			amount_to_send = int(input("How much would you like to send?"))
			recv_counter = self.wallet_a.synced_wallets[recieving_wallet]	#obtain the counter 
			self.wallet_a.balance = 100

			# only proceed if sufficient funds
			if amount_to_send <= int(self.wallet_a.balance):
				# Generate the token
				sending_token = self.check_length(self.wallet_a.ID) + self.check_length(recieving_wallet) + self.check_length(str(amount_to_send)) + self.check_length(str(recv_counter))
				print("sending token: ", sending_token)
				# Encrypt the token
				token = self.encrypt_token(sending_token)

				# Update wallet a 
				self.wallet_a.balance -= amount_to_send
			
				# display where the money's going 
				print("Transaction Sent. Wallet A's new balance: ", self.wallet_a.balance)
				# update B 
				self.receiving_funds(token)

				# Increment the counter in wallet a's table
				self.wallet_a.synced_wallets[recieving_wallet] += (recv_counter+1)
				break
			else: 
				print("Insufficient funds")
		

	# -----------------------------------------------------------
	# receiving_funds()- method for receiving funds from another wallet 
	#------------------------------------------------------------
	def receiving_funds(self, token):
		w_a, w_b, amount1, counter1 = self.decrypt_token(token)

		amount = self.find_amount(amount1)
		recieving_field = str(self.find_amount(w_b))
		a_counter_in_token = self.find_amount(counter1)
		a_counter_in_record = self.wallet_b.synced_wallets[self.wallet_a.ID]
		
		# validate that B's ID is in the receiver field
		# validate that the counter matches the record associate with wallet A in B's table 
		if (recieving_field == self.wallet_b.ID) and (a_counter_in_token == a_counter_in_record):
			# update wallet B's balance
			self.wallet_b.balance += amount

			# increment counter of A
			self.wallet_b.synced_wallets[self.wallet_a.ID] += (a_counter_in_record+1)

			# Display 
			print("Updated wallet B's balance: ", self.wallet_b.balance)
		else:
			print("Error in receiving funds. Please verify that the wallet IDs are accurate and are in their respective locations within the token.")
		self.option()
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
	def encrypt_token(self, info):
		cipher = AES.new(bytes.fromhex(self.KBank), AES.MODE_ECB)
		token = cipher.encrypt(bytes.fromhex(info)).hex()
		return token.upper() 

	# -----------------------------------------------------------
	# decrypt_token()- decrypts given token using AES.MODE_ECB
	#------------------------------------------------------------
	def decrypt_token(self,token):
		decipher = AES.new(bytes.fromhex(self.KBank), AES.MODE_ECB)
		result = decipher.decrypt(bytes.fromhex(token)).hex()
		w_a = result[:8]
		w_b = result[9:16]
		amount1 = result[17:24]
		counter1 = result[25:] 
		print("wallet a: ", w_a)
		print("wallet b: ", w_b)
		print("amount: ", amount1)
		print("counter: ", counter1)
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
