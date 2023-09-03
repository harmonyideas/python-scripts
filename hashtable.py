class MyHashTable(object):
    def __init__(self, size):
        self.my_table = ['Empty'] * size
        self.size = size

    def djb2_hash(self, s):
        hash = 0
        for x in str(s):
            hash = ((hash * 33) ^ ord(x))
        return hash

    def insert(self, key, data):
        key = (self.djb2_hash(key)) % self.size
        self.my_table[(key)] = data

    def getitem(self, key):
        key = self.djb2_hash(key) % self.size
        return self.my_table[key]

    def delete(self, key):
            key = self.djb2_hash(key) % self.size
            self.my_table[(key)] = 'Empty'


hash_table = MyHashTable(100)
hash_table.insert('Ping', 'Pong')
print hash_table.getitem('Ping')
hash_table.delete('Ping')
print hash_table.my_table





