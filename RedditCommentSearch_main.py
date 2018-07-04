import praw, webbrowser, sys
import subprocess as sp
from cryptography.fernet import Fernet
from os import path
from prawcore.exceptions import NotFound, BadRequest
from key_pathing import MasterKey as mk


k= 'keys/'

mk_found = mk.findMaster()
if mk_found == True:
	key_init = mk.initializeMaster()
else:
	sys.exit('No masterykey found, please run generate_keys.py first')

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
	decrypts[i] = str(key_init.decrypt(decrypt_key[i]))
	lens[i] = len(decrypts[i])
	ends[i] = lens[i] - 1

print(decrypts[2])

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

def formatList(lines_list):
	if len(lines_list) % 2 != 0:
		lines_list.append(" ")
	half = len(lines_list)//2
	sr_1 = lines_list[0:half]
	sr_2 = lines_list[half:]
	iterate = len(sr_1)
	for i in range(iterate):
		print('{0:<30s}{1}'.format(sr_1[i], sr_2[i]))


#ask user for string to search for in their comments.
while True:
	search_term = input('Enter search term: ')
	if search_term == '' or search_term.isspace():
		print('Search term cannot be empty')
	else:
		break


while True:
	sub_search = input('do you wish to search a specific subreddit? y/n : ')
	if sub_search == 'y':
		#generates a list of all subreddits user has commented it
		sr_output_file = path.isfile(f'output/{chooseuser}_subreddits.output')
		subreddits_list_raw = []
		subreddits_list = []
		if sr_output_file == False:
			print('generating subreddit list...')
			comments = user.comments.new(limit=None)
			for comment in comments:
				sr_commented = comment.subreddit.display_name	
				subreddits_list_raw.append(sr_commented)

			for i in subreddits_list_raw:
				if i not in subreddits_list:
					subreddits_list.append(i)

			sr_file = open(f'output/{chooseuser}_subreddits.output', 'a', encoding='utf-8')	
			for i in subreddits_list:
				sr_file.write(f'{i}\n')
			sr_file.close()
			formatList(subreddits_list)
		else:
			print('generating subreddit list...')
			lines_list = open(f'output/{chooseuser}_subreddits.output').read().splitlines()
			formatList(lines_list)

		search_subreddit = input('select a subreddit to search: ')
		try:
			r.subreddit(search_subreddit).random()
			break
		except NotFound:
			print('subreddit does not exist')
	elif sub_search == 'n':
		break
	else:
		print('please enter either y or n')

num_hits = 0

def saveOutput(comment_body, comment_permalink):
	global num_hits
	global text_file
	num_hits = num_hits + comment_body.count(search_term)
	text_file.write(f'--{comment_body}\n')
	text_file.write(f'  -url: {comment_permalink}\n\n')
	print(search_term, ': found in this comment', comment_body.count(search_term), 'time(s)')

text_file = open('output/'+f'{search_term}.output', 'a', encoding='utf-8')

#iterates over comments and checks for search_term's inclusion.
for comment in user.comments.new(limit=None):
	cb = comment.body
	cp = comment.permalink
	
	print(comment.body)
	if sub_search == 'y': # if sub_search is yes, only pick out comments from specified subreddit.
		if search_term in comment.body and str(comment.subreddit) == search_subreddit:
			saveOutput(cb, cp)
		else:
			print('could not find: '+ search_term+ ' in '+ search_subreddit)
	else: # sub_search is no, just check all comments.
		if search_term in comment.body:
			saveOutput(cb, cp)
		else:
			print('could not find: ', search_term)

text_file.close()

if num_hits > 1:
	print('\n'+'Found '+str(num_hits)+' hits')
else:
	print('\nSearch did not return any results')


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

m = input('press enter to close')
