import praw, string, re

from cryptography.fernet import Fernet

check_key = open('keys/'+'masterkey.key', 'r')
rkey = check_key.read()
cipher_suite = Fernet(rkey)

client_id_key = open('keys/'+'client_id_encoded.key', 'r').read().encode()
cid_decrypt = str(cipher_suite.decrypt(client_id_key))
cid_len = len(cid_decrypt)
cid_end = cid_len - 1

client_secret_key = open('keys/'+'client_secret_encoded.key', 'r').read().encode()
cs_decrypt = str(cipher_suite.decrypt(client_secret_key))
cs_len = len(cs_decrypt)
cs_end = cs_len - 1

username_key = open('keys/'+'username_encoded.key', 'r').read().encode()
un_decrypt = str(cipher_suite.decrypt(username_key))
un_len = len(un_decrypt)
un_end = un_len - 1

password_key = open('keys/'+'password_encoded.key', 'r').read().encode()
pw_decrypt = str(cipher_suite.decrypt(password_key))
pw_len = len(pw_decrypt)
pw_end = pw_len - 1

#checks your Reddit information in order to connect to Reddit API.
r = praw.Reddit(client_id= cid_decrypt[2:cid_end],
				client_secret= cs_decrypt[2:cs_end],
				user_agent='RedditCommentSearch',
				username= un_decrypt[2:un_end],
				password= pw_decrypt[2:pw_end])

#username of redditor whos comment history you want to search
user = r.redditor(un_decrypt[2:un_end])

#string you wish to search for in their comments
search_term = 'it'
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
	print(num_hits)
else:
	print('search did not return any results')

