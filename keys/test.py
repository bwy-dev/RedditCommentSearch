from cryptography.fernet import Fernet

check_key = open('key.key', 'r')
rkey = check_key.read()
cipher_suite = Fernet(rkey)

password_key = open('password_encoded.key', 'r').read().encode()
pw_decrypt = str(cipher_suite.decrypt(password_key))
pw_len = len(pw_decrypt)
pw_end = pw_len - 1

password= pw_decrypt[2:pw_end]

print(password)