import os
from os import path
from cryptography.fernet import Fernet


class MasterKey():

	def createMaster():
		key = Fernet.generate_key() 
		make_key_file = open('keys/masterkey.key', 'w')
		make_key_file.write(str(key)[2:46])
		make_key_file.close()

	def findMaster():
		base_path = path.dirname(__file__)
		key_file = path.isfile(path.join(base_path,'keys/masterkey.key'))
		if key_file == True:
			print('masterkey.key found in: '+str(path.join(base_path,'keys/masterkey.key')))
			return True
		elif key_file == False:
			print('masterkey not found, have you run generate_keys.py?')
			return False
		else:
			raise Exception('error, something has gone wrong here')#change soon, figure out possible errors

	def initializeMaster():
		check_key = open('keys/masterkey.key', 'r')
		rkey = check_key.read()
		key_init = Fernet(rkey)
		return key_init