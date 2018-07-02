import praw
import base64

#use base64.b64encode() to encode your password, print() it, and copy the resulting string into '' of b64decode. All this does is obfuscate\
#it so someone looking over your shoulder while you read or alter this file cannot see your reddit password\
#it does NOTHING to actually encrypt it if someone gains access to this file.
opw = base64.b64decode('')
dpw = opw.decode('utf-8')

r = praw.Reddit(client_id='',
				client_secret='',
				user_agent='',
				username= '',
				password= dpw)

#username of redditor whos comment history you want to search
user = r.redditor('')

#string you wish to search for in their comments
search_term = ''

num_hits = 0

#iterates over comments and checks for search_term's inclusion
for comment in user.comments.new(limit=None):
	print(comment.body)
	if search_term in comment.body:
		num_hits = num_hits + comment.body.count(search_term) #just a hit count for the end
		text_file = open(f"{search_term}.txt", "a")
		text_file.write(f'--{comment.body}\n')
		text_file.write(f'  -url: {comment.permalink}\n\n')
		text_file.close()
		print(search_term, ': found in this comment', comment.body.count(search_term), 'time(s)')
	else:
		print('could not find: ', search_term)

if num_hits > 1:
	print(num_hits)
else:
	print('search term did not return any results')

