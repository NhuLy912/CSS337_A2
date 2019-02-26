import hashlib
import sys
import os

def welcome():
  print("===========================")
  print("Welcome to Smart Wallet App")
  print("===========================")

def login():
  print("Login")

def signup():
  print("Signup")

def main_page():
  welcome()
  print("Please choose 1 option:\n\
    1 - Log In\n\
    2 - Sign Up\n")
  while True:
    option = input("Your choice: ")
    if option == "1":
      login()
      sys.exit()
    elif option == "2":
      signup()
      sys.exit()
    else:
      answer = input("Incorrect choice. Do you want to try again. Y(yes)/N(no): ")
      if answer == "N" or answer == "n":
        sys.exit()
    
def option():
  
  welcome()
  print("Please choose 1 option:\n\
  1 - Check Balance\n\
  2 - Receiving funds from the bank\n\
  3 - Synchronizing wallet\n\
  4 - Sending funds\n\
  5 - Receiving funds\n")
  while True:
    option = input("Your choice: ")
    if option == "1":
      check_balance()
      sys.exit()
    elif option == "2":
      funds_from_bank()
      sys.exit()
    elif option == "3":
      synchronizing_wallet()
      sys.exit()
    elif option == "4":
      sending_funds()
      sys.exit()
    elif option == "5":
      receiving_funds()
      sys.exit()
    else:
      answer = input("Incorrect choice. Do you want to try again. Y(yes)/N(no): ")
      if answer == "N" or answer == "n":
        sys.exit()

def check_balance():
  print("Option 1")
  with open("wallet.txt", "a") as myfile:
    myfile.write("appended text")

def funds_from_bank():
  print("Option 2")

def synchronizing_wallet():
  print("Option 3")

def sending_funds():
  print("Option 4")

def receiving_funds():
  print("Option 5")

# calculate k_wallet
def SHA_256(student_id):
  k_wallet = hashlib.sha256(student_id.encode()).hexdigest()
  return k_wallet

def main():
  
  option()
  #age = input("What is your age? ")
  #print("Your age is: ", age)

  student_id = "56789859"
  k_wallet = SHA_256(student_id)
  print(k_wallet.upper())

if __name__ == '__main__':
    main()