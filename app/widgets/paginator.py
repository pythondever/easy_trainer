class Paginator:
    def __init__(self, items, page_size):
        self.items = items
        self.page_size = page_size

    def __getitem__(self, index):
        return Page(self.items, self.page_size, index)
        # return self.items[index * self.page_size: index * self.page_size + self.page_size]

    def __iter__(self):
        return Pages(self.items, self.page_size)


class Pages:
    def __init__(self, items, page_size):
        self.items = items
        self.page_size = page_size
        self.index = 0

    def __next__(self):
        if self.index * self.page_size >= len(self.items): raise StopIteration
        self.index = self.index + 1
        return Page(self.items, self.page_size, self.index - 1)


class Page:
    def __init__(self, items, page_size, index):
        total = len(items)
        begin = index * page_size
        end = index * page_size + page_size

        self.items = items[begin: end]
        self.has_prev = (begin > 0)
        self.has_next = end < total
        self.index = index

    def __iter__(self):
        return Items(self.items)


class Items:
    def __init__(self, items):
        self.items = items
        self.index = 0

    def __next__(self):
        if self.index >= len(self.items): raise StopIteration
        self.index = self.index + 1
        return self.items[self.index - 1]


def test():
    paginator = Paginator(range(100), 4)
    for i in paginator[0]:
        print(i)


if __name__ == "__main__":
    test()