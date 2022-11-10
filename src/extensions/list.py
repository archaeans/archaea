
class List(list):
    def __getitem__(self, key):
        return list.__getitem__(self, key)

    def cons(self):
        return [[list[i], list[i + 1]]
                for i in range(len(list) - 1)]
