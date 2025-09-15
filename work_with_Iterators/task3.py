from re import S


class FlatIterator:

    def __init__(self, list_):
        self.list_ = list_
        self.subarray_index = 0
        self.item_index = 0
        self.stack = []

    def __iter__(self):
        return self

    def __next__(self):
        if self.stack:
            item = self.stack.pop(0)
            if isinstance(item, list):
                self.stack = item + self.stack
                return self.__next__()
            return item

        if self.item_index == len(self.list_[self.subarray_index]):
            self.subarray_index += 1
            if self.subarray_index == len(self.list_):
                raise StopIteration
            self.item_index = 0
        item = self.list_[self.subarray_index][self.item_index]
        if isinstance(item, list):
            if item:
                self.stack.extend(item)
            self.item_index += 1
            return self.__next__()

            
        self.item_index += 1
        return item


def test_3():

    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):

        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']


if __name__ == '__main__':
    test_3()