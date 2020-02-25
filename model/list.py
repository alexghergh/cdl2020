class IndexList():
    """This class is a modified list. It holds lists of 1's and 0's.

    It holds a regular list object that contains only 1's and 0's (representing
    whether a word appears in a file or not), but adds functionality through
    the overriden operators &, | and ~, which mean:
    & - AND between 2 lists
    | - OR between 2 lists
    ~ - INVERT a list's objects

    """

    def __init__(self, lst):
        """Initialize the self object with a regular list of 1's and 0's passed
        as parameter, representing whether a word from the index appears or not
        in a file.

        Example:
            'from': [1, 0, 0, 1]
            The word 'from' appears in files 1 and 4.

        Args:
            lst: The list object with the meaning detailed above.

        Important: The list object passed as parameter is only meant to be
        created inside the Index class. See Index in 'index.py' for more
        information.

        """
        # check that indeed the list passed as parameter contains only 1's and 0's
        if not all(item in [1, 0] for item in lst):
            raise ValueError("[Error] IndexList contains values different from 1 and 0.")
        self._lst = lst

    @property
    def lst(self):
        """Simple getter for the list object.

        Returns:
            The list containing 1's and 0's.
        """
        return self._lst

    def __and__(self, other):
        """AND between 2 IndexList objects. What it does is take 2 IndexList
        objects and AND's each element in the first and second list
        respectively.

        Example:
            lst1: [1, 0, 1, 0]
            lst2: [0, 1, 1, 1]
            lst1 & lst2 = [0, 0, 1, 0]

        Args:
            other: Since AND is a binary operation, other is the second
            argument needed for that.

        Returns:
            An IndexList, so chaining multiple operations is possible.

        """
        lst = [1 if i == 1 and j == 1
               else 0
               for i, j in zip(self._lst, other.lst)]
        return IndexList(lst)

    def __or__(self, other):
        """OR between 2 IndexList objects. What it does is take 2 IndexList
        objects and OR's each element in the first and second list
        respectively.

        Example:
            lst1: [1, 0, 0, 1]
            lst2: [0, 1, 0, 1]
            lst1 | lst2 = [1, 1, 0, 1]

        Args:
            other: Since OR is a binary operation, other is the second argument
            needed for that.

        Returns:
            An IndexList, so chaining multiple operations is possible.

        """
        lst = [1 if i == 1 or j == 1
               else 0
               for i, j in zip(self._lst, other.lst)]
        return IndexList(lst)

    def __invert__(self):
        """INVERT an IndexList object. What it does is take an IndexList object
        and INVERT every element in it.

        Example:
            lst1: [1, 0, 0, 1]
            ~lst1 = [0, 1, 1, 0]

        Returns:
            An IndexList, so chaining multiple operations is possible.

        """
        lst = [0 if i == 1 else 1 for i in self._lst]
        return IndexList(lst)

    def __iter__(self):
        """Return an iterable object.

        Returns:
            An iterable from the list object.

        """
        return iter(self._lst)

    def __str__(self):
        """String representation of an IndexList object.

        Returns:
            The string representation of the class.

        """
        return f'IndexList({str(self._lst)})'
