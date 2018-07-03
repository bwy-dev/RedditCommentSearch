import praw, re, webbrowser
import subprocess as sp
from cryptography.fernet import Fernet
from os import path
from prawcore.exceptions import NotFound, BadRequest
from key_pathing import KeyPathing as kp

k= 'keys/'

cipher_suite = kp.findmaster()

#get encrypted keys from their .key files.

client_id_key = open(k+'client_id_encoded.key', 'r').read().encode()
client_secret_key = open(k+'client_secret_encoded.key', 'r').read().encode()
username_key = open(k+'username_encoded.key', 'r').read().encode()
password_key = open(k+'password_encoded.key', 'r').read().encode()

#iterates over the keys, decrypting them, then working out their length to remove the ''s from them.
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

#asks user to enter a Reddit username whos comments the script will look through.
while True:
	chooseuser = input('Select user to search: ')
	try:
		if getattr(r.redditor(chooseuser), 'is_suspended', False): #checks to see if the redditor is suspended.
			print('user is suspended')
	except NotFound:# if not suspended, does it throw a NotFound exception?
		print('user does not exist')
	except BadRequest:# if what is entered isnt a valid username (eg. contains punctuation) throw BadRequest exception.
		print('please enter a valid username')
	else:
		user = r.redditor(chooseuser)# if none of these, reddior exists, continue on to search term input.
		break


#ask user for string to search for in their comments.
search_term = input('Enter search term: ')

num_hits = 0

#iterates over comments and checks for search_term's inclusion.
for comment in user.comments.new(limit=None):
	print(comment.body)
	if search_term == '' or search_term.isspace(): #throws exception if search_term is empty.
		raise Exception('Search term cannot be empty')
	elif search_term in comment.body:
		num_hits = num_hits + comment.body.count(search_term) #just a hit count for the end.
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
