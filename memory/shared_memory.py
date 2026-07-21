class SharedMemory:


    def __init__(self):

        self.storage = {}



    def set(self, key, value):

        self.storage[key] = value



    def get(self, key, default=None):

        return self.storage.get(
            key,
            default
        )



    def append(self, key, value):

        if key not in self.storage:

            self.storage[key] = []


        self.storage[key].append(value)



    def all(self):

        return self.storage