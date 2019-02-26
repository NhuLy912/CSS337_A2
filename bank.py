import hashlib
from Crypto.Cipher import AES

#B751237F9A7ED3530A67CEBD5E18816387C0A372A9E1D424A5F276A997FB6252
def SHA_256(student_id):
  k_wallet = hashlib.sha256(student_id.encode()).hexdigest()
  return k_wallet

def EMD():
  emd = "D8D9752ED5CCCB9F460FB8D6EB86A984"
  k = "CF959C7BFC4FB5792AA25457578EF9E8B78E3558A8B7BF6A92338397B5F4639D"
  decipher = AES.new(bytes.fromhex(k), AES.MODE_ECB)
  result = decipher.decrypt(bytes.fromhex(emd)).hex()
  print(result)

def check_length(value):
  if len(value) != 8:
    while True:
      if len(value) == 8:
        return value
      else:
        value = "0" + value
  return value

def encrypt_token():
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

def decrypt_token(token):
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

def table_sync(sender, amount, counter):
  print("\n   Table sync")
  sender = sender.strip("0")
  print("\tSender", sender)
  print("\tAmount", amount)
  print("\tCounter", counter)
  print("Writing to file")
  #with open("wallet_A.txt", "a") as myfile:
  #  myfile.write(sender + " " + str(int(counter) + 2) + "\n")

def Synchronizing(token):
  w_a, w_b, amount1, counter1 = decrypt_token(token)
  print("Synchronizing")
  print(" Sender: ", w_a)
  print(" Receiver: ", w_b)
  table_sync(w_a, "00000000", "00000000")

def main():
  print("\n============= SHA_256 ===================\n")
  student_id = "56789859"
  k_wallet = SHA_256(student_id)
  print("K_wallet main:\n", k_wallet)

  print("\n=========== EMD : AES_256 ===============\n")
  EMD()

  print("\n========== Encrypt token ============\n")
  encrypt_token()

  #print("\n========== Decrypt token ============\n")
  #decrypt_token()

  print("\n===== Synchronizing W_B -> W_A========\n")
  Synchronizing("965390DFD8B18BCD419CA0583896218A")

  print("\n===== bank wallets========\n")
  with open("Bank.txt") as myfile:
    for line in myfile:
      print(line)

if __name__ == '__main__':
    main()