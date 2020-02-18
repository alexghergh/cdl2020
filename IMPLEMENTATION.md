## This file contains the implementation details of the problem

First of all, we have a `model` directory that contains our data structures.

Those are the Index itself and the IndexList.

Some details about what each one does:

#### Index

The index holds 2 things:

1. A list of the file names added to the index so far.
2. A dictionary that holds words as keys, and lists of file names as values.

For how one such dictionary looks like, see the [index.py](model/index.py) file.

#### IndexList

The IndexList holds a regular list of 1's and 0's, representing whether a word appears in a file or not.

For more info on this see [list.py](model/list.py).

### Algorithm

The algorithm is simple enough. First we see if there is a `files.txt`. If there is, we scan the file names from it. If there is not, we read them from the input.

After that, we build the index by scanning every word and seeing if it already is in the index; if not, we add it, together with a list that contains the file name in which it appeared.

The next step is solving the query:

We do this with the help of the IndexList class. Its &, | and ~ operators are overriden, so they mean &&, || and ! respectively.

Example:
If we have 2 IndexLists, we can do this:

`IndexList([1, 0, 1]) | IndexList([1, 1, 0]) = IndexList([1, 0, 0])`

(because `[1, 0, 1] || [1, 1, 0]` is indeed `[1, 0, 0]`).

We use the Index class to transform the query into these IndexLists, like this example:

Query: `from || !(source) && (kernel || input)` - find the files that contain `from` and `kernel` or `input`, but don't contain `source`.

Every word gets transformed into its corresponding IndexList:

`IndexList([1, 0, 1]) | ~IndexList([1, 1, 0]) & (IndexList([1, 1, 0]) | IndexList([0, 0, 0]))`

(assuming `from` appears in files 1 and 3, `source` appears in files 1 and 2, `kernel` appears in files 1 and 2, and `input` doesn't appear in any file).

and then it gets executed by Python's [eval](https://docs.python.org/3/library/functions.html#eval) function, and the result is returned as an IndexList, which then gets transformed into a normal list, from which files get extracted and given back to the user.

Of course, the algorithm is not limited to 3 files.
