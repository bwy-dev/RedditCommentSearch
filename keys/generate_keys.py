#If you are using RedditCommentSearch yourself you will currently have to run this script first to generate the necessary keys to run the program

from cryptography.fernet import Fernet
from os import path

base_path = path.dirname(__file__)

key_file = path.isfile(path.join(base_path,'masterkey.key'))

if key_file == False: #if masterkey doesn't exist, generate it
	key = Fernet.generate_key() 
	make_key_file = open('masterkey.key', 'w')
	make_key_file.write(str(key)[2:46])
	make_key_file.close()
else:
	pass

#opens the master key
check_key = open('masterkey.key', 'r')
rkey = check_key.read()
cipher_suite = Fernet(rkey)

#add necessary info in between the '' here
client_id_encoded = cipher_suite.encrypt(b'')
client_secret_encoded = cipher_suite.encrypt(b'')
password_encoded = cipher_suite.encrypt(b'')
username_encoded = cipher_suite.encrypt(b'')

encoded_info = {client_id_encoded : 'client_id_encoded', client_secret_encoded : 'client_secret_encoded', password_encoded : 'password_encoded',
username_encoded : 'username_encoded'}

#writes a .key file for each value
for x, y in encoded_info.items():
	write_key_file = open(f'{y}.key', 'w')
	x_length = len(str(x))
	r_end = x_length - 1
	write_key_file.write(str(x)[2:r_end])
	write_key_file.close()


#print(client_id_decoded)