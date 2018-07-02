## Reddit Comment Search

>This simple script is used to search a users comment for a specific string, and then prints comments containing that string, and the permalink for the comment, to a .txt.
> I will be updating this regularly to make it more robust and add additional functionality, and possibly a GUI. This is more of a personal project for me, but I will be
> documenting my progress and the usage of this script incase any one wants to follow along or use it themselves.

#### To do list:

1. include ability to search for an explicit word or phrase, as opposed to searching for a string (e.g. currently searching "in" would return all occurrences of the word "f*in*ish" too)
2. move the private keys as well as passwords to an encrypted file for security, reference them from there.
3. add the ability to search specific subreddits, or posts written in specific timespans.
4. add a GUI, or integrate this into a website if features become useful enough to warrant it.

#### Limitations:

- The Reddit API only allows to search the last 1000 comments left by a user.

#### Requirements:

- A Reddit account.
- [praw](https://github.com/praw-dev/praw) to interact with the reddit API with Python.
- [OAuth Authentication](https://praw.readthedocs.io/en/latest/getting_started/authentication.html#oauth) praw has a tutorial on this in the docs


*readme will be updated more at a later date *