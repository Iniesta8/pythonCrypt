#!/usr/bin/env python

# from cryptography.fernet import Fernet
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import sys, random, os

# key = Fernet.generate_key()
# cipher_suite = Fernet(key)
chunk_size = 64 * 1024

def encryptMessage(key, filename):
	outputFilename = "encrypted_" + filename
	filesize = str(os.path.getsize(filename)).zfill(16)
	iv = ""

	for i in range(16):
		iv += chr(random.randint(0, 0xFF))

	encryptor = AES.new(key, AES.MODE_CBC, iv)

	with open(filename, "rb") as inf:	
		with open(outputFilename, "wb") as outf:
			outf.write(filesize)
			outf.write(iv)
			while True:
				message_chunk = inf.read(chunk_size)
				if len(message_chunk) == 0:
					break
				elif len(message_chunk)%16 != 0:
					message_chunk += ' ' * (16 - (len(message_chunk) % 16))

				outf.write(encryptor.encrypt(message_chunk))


def decryptMessage(key, filename):
	outputFilename = "decrypted_" + filename
	with open(filename, "rb") as inf:
		filesize = long(inf.read(16))
		iv = inf.read(16)

		decryptor = AES.new(key, AES.MODE_CBC, iv)

		with open(outputFilename, "wb") as outf:
			while True:
				message_chunk = inf.read(chunk_size)

				if len(message_chunk) == 0:
					break
				outf.write(decryptor.decrypt(message_chunk))
			outf.truncate(filesize)


# def encryptMessage2(filename):
# 	outputFilename = "encrypted_" + filename
# 	filesize = str(os.path.getsize(filename)).zfill(16)
# 	with open(filename, "rb") as inf:	
# 		with open(outputFilename, "wb") as outf:
# 			outf.write(filesize)
# 			while True:
# 				message_chunk = inf.read(chunk_size)
# 				if len(message_chunk) == 0:
# 					break
# 				elif len(message_chunk)%16 != 0:
# 					message_chunk += ' ' * (16 - (len(message_chunk) % 16))

# 				outf.write(cipher_suite.encrypt(message_chunk))

# def decryptMessage2(filename):
# 	outputFilename = "decrypted_" + filename
# 	with open(filename, "rb") as inf:
# 		filesize = long(inf.read(16))

# 		with open(outputFilename, "wb") as outf:
# 			while True:
# 				message_chunk = inf.read(chunk_size)

# 				if len(message_chunk) == 0:
# 					break
# 				outf.write(cipher_suite.decrypt(message_chunk))
# 			outf.truncate(filesize)

def getKey(password):
	h = SHA256.new(password)
	return h.digest()

def Main():
	choice = raw_input("Do you want to [e]ncrpyt or [d]ecrypt a file?  ")

	if choice == 'e' or choice == 'E':
		filename = raw_input("File to encrypt: ")
		password = raw_input("Password: ")
		encryptMessage(getKey(password), filename)
		# encryptMessage2(filename)
		print "Encryption done. Encrypted message saved in \"encrypted_" + filename + "\"."

	elif choice == 'd' or choice == 'D':
		filename = raw_input("File to decrypt: ")
		password = raw_input("Password: ")
		decryptMessage(getKey(password), filename)
		# decryptMessage2(filename)
		print "Decryption done. Decrypted message saved in \"decrypted_" + filename + "\"."

	else:
		print "No valid choice, exit..."

if __name__=="__main__":
	Main()


