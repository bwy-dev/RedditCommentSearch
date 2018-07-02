import praw, string, re, webbrowser
import subprocess as sp
from cryptography.fernet import Fernet
from os import path

base_path = path.dirname(__file__)
key_file = path.isfile(path.join(base_path,'keys/masterkey.key'))

kf= 'keys/'

if key_file == True: #checks if masterkey.key has been generated yet
	check_key = open(kf+'masterkey.key', 'r')
	rkey = check_key.read()
	cipher_suite = Fernet(rkey)
else:
	raise Exception('masterkey.key does not exist! Run keys/generate_keys.py before running RedditCommentSearch.py')

#get encrypted keys from their .key files
client_id_key = open(kf+'client_id_encoded.key', 'r').read().encode()
client_secret_key = open(kf+'client_secret_encoded.key', 'r').read().encode()
username_key = open(kf+'username_encoded.key', 'r').read().encode()
password_key = open(kf+'password_encoded.key', 'r').read().encode()

#iterates over the keys, decrypting them, then working out their length to remove the ''s from them
decrypt_key = [client_id_key, client_secret_key, username_key, password_key]
decrypts = [''] *4 
lens = [0] *4
ends = [0] *4
for i in range(3):
	decrypts[i] = str(cipher_suite.decrypt(decrypt_key[i]))
	lens[i] = len(decrypts[i])
	ends[i] = lens[i] - 1

#checks your Reddit information in order to connect to Reddit API.
r = praw.Reddit(client_id= decrypts[0][2:ends[0]],
				client_secret= decrypts[1][2:ends[1]],
				user_agent='RedditCommentSearch',
				username= decrypts[2][2:ends[2]],
				password= decrypts[3][2:ends[3]])

#username of redditor whos comment history you want to search, while this is currently set to the users, it can be any usename you wish
user = r.redditor(decrypts[2][2:ends[2]])

#ask user for string to search for in their comments
search_term = input('Enter search term: ')

num_hits = 0

#iterates over comments and checks for search_term's inclusion
for comment in user.comments.new(limit=None):
	print(comment.body)
	if search_term == '' or search_term.isspace(): #throws exception if search_term is empty
		raise Exception('Search term cannot be empty')
	elif search_term in comment.body:
		num_hits = num_hits + comment.body.count(search_term) #just a hit count for the end
		text_file = open('output/'+f'{search_term}.output', 'a', encoding='utf-8')
		text_file.write(f'--{comment.body}\n')
		text_file.write(f'  -url: {comment.permalink}\n\n')
		text_file.close()
		print(search_term, ': found in this comment', comment.body.count(search_term), 'time(s)')
	else:
		print('could not find: ', search_term)

if num_hits > 1:
	print('\n'+'Found '+str(num_hits)+' hits')
else:
	print('\nSearch did not return any results')

islooping = True

while True:
	done = input('would you like to open output file in notepad?: y/n: ')
	if done == 'y':
		programName = 'notepad.exe'
		fileName = 'output/'+f'{search_term}.output'
		sp.Popen([programName, fileName])
		break
	elif done == 'n':
		break
	else:
		print('please enter either y or n')

m = input('press enter to exit')
