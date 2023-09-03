import hashlib

# Truncate to 6 digits 
hashnum = int(hashlib.sha1("Hello, World").hexdigest(), 16) % (10 ** 6)
print(hashnum)
