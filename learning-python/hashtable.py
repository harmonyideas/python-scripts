class MyHashTable():
    def __init__(self, size):
        self.my_table = ['Empty'] * size
        self.size = size

    def djb2_hash(self, s):
        hash_value = 5381
        for x in str(s):
            hash_value = ((hash_value << 5) + hash_value) + ord(x)
        return hash_value % self.size

    def insert(self, key, data):
        key_hash = self.djb2_hash(key)
        self.my_table[key_hash] = data

    def getitem(self, key):
        key_hash = self.djb2_hash(key)
        return self.my_table[key_hash]

    def delete(self, key):
        key_hash = self.djb2_hash(key)
        self.my_table[key_hash] = 'Empty'


hash_table = MyHashTable(100)
hash_table.insert('Ping', 'Pong')
print(hash_table.getitem('Ping'))
hash_table.delete('Ping')
print(hash_table.my_table)
