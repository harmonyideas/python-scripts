my_table = ['Empty'] * 100

def djb2_hash(s):
    hash = 5138
    for x in str(s):
        hash = ((hash << 5) + hash) + ord(x)
    return hash % 100


def insert(key,data):
    key = djb2_hash(key)
    my_table[(key)] = data


def getitem(key):
    key = djb2_hash(key)
    return my_table[key]


insert(186,'TEST')
print getitem(186)
print my_table



