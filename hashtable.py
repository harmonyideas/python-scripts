my_table = ['Empty'] * 100

def djb2_hash(s):
    hash = 0
    for x in str(s):
        hash = ((hash * 33) ^ ord(x)) % 100
    print hash
    return hash


def insert(key,data):
    key = djb2_hash(key)
    my_table[(key)] = data


def getitem(key):
    key = djb2_hash(key)
    return my_table[key]


insert('Ping','Pong')
print getitem('Ping')





