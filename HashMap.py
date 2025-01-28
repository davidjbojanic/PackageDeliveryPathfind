class HashMap:
    def __init__(self, initial_size=64):
        # Initialize the hash map with a default size and empty buckets
        self.size = initial_size
        self.data = [None] * self.size # Buckets stored as lists (chaining)

    # Method to generate a hash index by summing ASCII values of the key's characters
    def get_hash(self, key):
        hash = 0
        for char in str(key):
            hash += ord(char)
        return hash % self.size # Modulo ensures the index fits within the current size

    def add(self, key, value):
        # Check if resize is needed before adding (threshold: load factor >= 0.75)
        if self.get_load_factor() >= 0.75:
            self.resize()

        key_hash = self.get_hash(key)
        key_value = [key, value] # Store key-value as pair

        # If bucket is empty, initialize with the new pair
        if self.data[key_hash] is None:
            self.data[key_hash] = [key_value]
            return True

        # If key exists in bucket; update its value
        for pair in self.data[key_hash]:
            if pair[0] == key:
                pair[1] = value
                return True

        # If key doesn't exist in bucket; append to chain
        self.data[key_hash].append(key_value)

    # Method to double the size of the data array and rehash all entries
    def resize(self):
        old_data = self.data
        self.size *= 2
        self.data = [None] * self.size

        # Rehash each entry into the new array
        for bucket in old_data:
            if bucket is not None:
                for pair in bucket:
                    key, value = pair
                    key_hash = self.get_hash(key) # Recompute hash with new size
                    if self.data[key_hash] is None:
                        self.data[key_hash] = [pair]
                    else:
                        self.data[key_hash].append(pair)

    # Method to retrieve the value for a key by searching its bucket's chain
    def get(self, key):
        key_hash = self.get_hash(key)
        if self.data[key_hash] is not None:
            for pair in self.data[key_hash]:
                if pair[0] == key:
                    return pair[1]
        return None # Key not found

    # Method to calculate the current load factor (items/buckets)
    def get_load_factor(self):
        items = 0
        for bucket in self.data:
            if bucket is not None:
                items += len(bucket)
        load_factor = items / len(self.data)
        return load_factor

    # Method to return the input key if it exists in the map
    def get_key(self, key):
        key_hash = self.get_hash(key)
        if self.data[key_hash] is not None:
            for pair in self.data[key_hash]:
                if pair[0] == key:
                    return pair[0]



