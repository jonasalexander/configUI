import hashlib

def checkPassword(input):
	print "Checking password..."
	return saltAndHash(input) == saltAndHash(user_password)

def saltAndHash(password):
	print "Hashing and salting \"%s\"..." %password
	salt = "-WOu@p.Za,>W+6&`A63/"
	sha1 = hashlib.sha1()
	sha1.update(password + salt)
	return sha1.hexdigest()

# user_password = saltAndHash("peRgiB16901")

# MARK: Development

user_password = saltAndHash("pword")