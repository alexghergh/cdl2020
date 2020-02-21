## This file contains the implementation details of the problem

First of all, we have a `model` directory that contains our data structures.

Those are the Index itself and the IndexList.

Some details about what each one does:

#### Index

The index holds 2 things:

1. A list of the file names added to the index so far.
2. A dictionary that holds words as keys, and lists of integers representing files as values.

For how one such dictionary looks like, see the [index.py](model/index.py) file.

#### IndexList

The IndexList holds a regular list of 1's and 0's, representing whether a word appears in a file or not.

For more info on this see [list.py](model/list.py).

There is also a `config` directory holding information about external configuration, that has a Config class with the following meaning.

#### Config

The Config class reads the `config.json` configuration file and makes it easily accesible to the program through a Python dictionary.

For more info see [config.py](config/config.py).

### Algorithm

The algorithm is simple enough. First we see if there is a `files.txt`. If there is, we scan the file names from it. If there is not, we read them from the input.

After that, we construct a set of words from every file one at a time, remove the stop words if we need to, apply the stemming algorithm if stemming is enabled, and build the index with the words from the set.

The next step is solving the query:

We do this with the help of the IndexList class. Its &, | and ~ operators are overriden, so they mean &&, || and ! respectively.

Example:  
If we have 2 IndexLists, we can do this:

`IndexList([1, 0, 1]) | IndexList([1, 1, 0]) = IndexList([1, 0, 0])`

(by evaluating every term in order in `[1, 0, 1] || [1, 1, 0]` we indeed get `[1, 0, 0]` as a result).

We use the Index class to transform the query into these IndexLists, like this example:

Query: `from || !(source) && (kernel || input)` - find the files that contain `from` and `kernel` or `input`, but don't contain `source`.

Every word gets transformed into its corresponding IndexList (by scanning the index we built earlier):

`IndexList([1, 0, 1]) | ~IndexList([1, 1, 0]) & (IndexList([1, 1, 0]) | IndexList([0, 0, 0]))`

(assuming `from` appears in files 1 and 3, `source` appears in files 1 and 2, `kernel` appears in files 1 and 2, and `input` doesn't appear in any file).

After this, the query gets executed by Python's [eval](https://docs.python.org/3/library/functions.html#eval) function and the result is returned as an IndexList, which then gets transformed into a normal list, from which files get extracted and given back to the user.

Of course, the algorithm is not limited to 3 files, nor it is limited to 4 parameters in the query.
