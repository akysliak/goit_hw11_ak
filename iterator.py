def __init__(self, collection, n=None):
    """
    Initializes the iterator.
    :param collection: collection over with the iterator will iterate. Expected: dict with records.
    :param n: number of objects from the collection which have to be returned in one iteration.
                If None, all objects will be returned at once.
    """
    print("in init")
    self.__collection = collection
    self.__n = n


@property
def collection(self):
    return self.__collection


@collection.setter
def collection(self, new_collection):
    """
    Validates and sets a new collection to iterate over.
    :param new_collection: new collection
    """
    if not new_collection or isinstance(new_collection, Iterable):
        self.__collection = new_collection
    else:
        raise ValueError(f"The collection {new_collection} for iteration is not iterable.")


@property
def n(self):
    return self.__n


@n.setter
def n(self, new_n: int):
    """
    Validates and sets a new value for the parameter "n": number of elements returned in one iteration.
    Throws an exception if the new value is not valid: must be a positive integer number.
    :param new_n: new value for the parameter "n".
    """
    try:
        new_n = int(new_n)
        if new_n <= 0:
            raise MyException()
        self.__n = new_n
    except:
        raise MyException(f"Positive integer number is expected as a parameter for iteration, provided: '{new_n}")


def __iter__(self):
    print("in iter")
    return ABIterator(self.__collection, self.__n)


def __next__(self):
    print("in next")
    # raise StopIteration

    if not self.__collection:
        raise StopIteration
    elif not self.__n:
        yield "hello"  # self.__collection
        raise StopIteration
    else:
        raise StopIteration
        res = []
        for el in self.__collection:
            res.append(el)
            if len(res) == self.__n:
                yield res
                res = []
        if res:
            yield res
        raise StopIteration


class ABIterator2:
    def __init__(self):
        self.data = [1, 2, 3]

    def __iter__(self):
        return self

    def __next__(self):
        print("in next")
        raise StopIteration

# depr from fields Birthday reformat_value
'''
if len(day) != 2:
    day = int(day)
    day = str(day) if day >= 10 else f"0{day}"
if len(month) != 2:
    month = int(month)
    month = str(month) if month >= 10 else f"0{month}"
date = f"{day}/{month}"
return date
'''