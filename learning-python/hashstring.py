import hashlib

# Truncate to 6 digits 
hashnum = int(hashlib.sha256("Hello, World".encode('utf-8')).hexdigest(), 16) % (10 ** 6)
print(hashnum)
