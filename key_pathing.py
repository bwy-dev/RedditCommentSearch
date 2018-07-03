from os import path
from cryptography.fernet import Fernet


class KeyPathing():

	def genkey():
		key = Fernet.generate_key() 
		make_key_file = open('keys/masterkey.key', 'w')
		make_key_file.write(str(key)[2:46])
		make_key_file.close()

	def findmaster():
		base_path = path.dirname(__file__)
		key_file = path.isfile(path.join(base_path,'keys/masterkey.key'))
		if key_file == False:
			while True:
				print('masterkey does not exist, it might not have been generated or it might not exist yet')
				q = input('create masterkey? y/n: ')
				if q == 'y':
					KeyPathing.genkey()
					print('masterkey generated')
					break
				elif q == 'n':
					break
				else:
					print('please enter y or n')

		elif key_file == True:
			check_key = open('keys/masterkey.key', 'r')
			rkey = check_key.read()
			cipher_suite = Fernet(rkey)
			return cipher_suite
		else:
			raise Exception('something has gone horribly wrong')

	