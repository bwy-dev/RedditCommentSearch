#If you are using RedditCommentSearch yourself you will currently have to run this script first to generate the necessary keys to run the program

from cryptography.fernet import Fernet
from os import path
import getpass
from key_pathing import KeyPathing as kp

cipher_suite = kp.findmaster() #findmaster in key_pathing.py looks for masterkey, then initializes it.

client_id= input('Enter your client Id: ').strip().encode()
client_secret = input('Enter your client secret: ').strip().encode()
username = input('Enter your Reddit username: ').strip().encode()
password = getpass.getpass('Enter your Reddit Password: ').encode()


client_id_encoded = cipher_suite.encrypt(client_id)
client_secret_encoded = cipher_suite.encrypt(client_secret)
password_encoded = cipher_suite.encrypt(password)
username_encoded = cipher_suite.encrypt(username)

encoded_info = {client_id_encoded : 'keys/client_id_encoded', client_secret_encoded : 'keys/client_secret_encoded', password_encoded : 'keys/password_encoded',
username_encoded : 'keys/username_encoded'}

#writes a .key file for each value
for x, y in encoded_info.items():
	write_key_file = open(f'{y}.key', 'w')
	x_length = len(str(x))
	r_end = x_length - 1
	write_key_file.write(str(x)[2:r_end])
	write_key_file.close()

print('success, encrypted keys have been created')
input('press enter to close')