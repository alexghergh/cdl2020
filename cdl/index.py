from collections import defaultdict
from cdl.list import IndexList
import re

# TODO refactor so the class returns the strings rather than printing them
# this is so a GUI can use the class as well


class Index():
    """This class is meant to hold information about the index.

    The way we hold an index is through these 2 fields:
      1. files: A list keeping the names of the files scanned so far.
      2. index: A dictionary that holds words as keys, and the files
      they appear in as values. The values are lists of integers representing
      the files a word appears in.

    """

    def __init__(self):
        """Initialization of the index.

        _files: Initialize the files to an empty list.

        _index: The index has a structure like this:
            {
                'from': ['doc1', 'doc2'],
                'kernel': ['doc1'],
                'c': ['doc2', 'doc3']
            }
        where 'from', 'kernel' and 'c' are words from the documents.
        It actually uses a defaultdict instead of a regular dict, but the
        result is the same.

        _regex: A regex expression to match words only, since that is what
        we're interested in.

        """
        self._files = []
        self._index = defaultdict(list)
        self._regex = re.compile(r'\w+')

    def add_file(self, file_name):
        """Scan a file and add the words to the index.

        Args:
            file_name: The file to be scanned.

        """
        # Return if file was already scanned
        if file_name in self._files:
            print('[Error] The file is already in the index!')
            return

        try:
            # Open the file, add it to the _files list, then apply the
            # regex to every line in it
            with open(file_name) as file:
                self._files.append(file_name)
                for line in file:
                    matches = self._regex.findall(line)
                    for match in matches:
                        if file_name not in self._index[match.lower()]:
                            self._index[match.lower()].append(file_name)
        except FileNotFoundError:
            raise FileNotFoundError('[Error] File does not exist!')
            #  print('[Error] File does not exist!')
        except IsADirectoryError:
            raise IsADirectoryError('[Error] That is a directory!')
            #  print('[Error] That is a directory!')
        except PermissionError:
            raise PermissionError('[Error] Permission denied!')
            #  print('[Error] Permission denied!')
        except Exception as e:
            raise Exception('An error occured: ', e)
            #  print('An error occurred: ', e)
        else:
            return '[Success] File was added to index!'
            #  print('[Success] File was added to index!')

    def _get_index_list_for_word(self, word):
        """This function returns an IndexList associated with a word.
        For more info see IndexList in 'list.py'.

        Args:
            word: The word to return an IndexList for.

        """
        word_list = [1 if file in self._index[word.lower()]
                     else 0
                     for file in self._files]
        return IndexList(word_list)

    def get_result_for_query(self, query):
        """This function returns a result for a query.

        Args:
            query: The query to return a result for.

        """
        # Replace every word with the corresponding IndexList object
        query = self._regex.sub(
                lambda match:
                str(self._get_index_list_for_word(match.group(0))),
                query)

        # Replace && with &, || with |, and ! with ~
        query = re.sub(r'\s*&&\s*', ' & ', query)
        query = re.sub(r'\s*\|\|\s*', ' | ', query)
        query = re.sub(r'\s*!', ' ~', query)

        # If the query is not empty, return the files that match the query
        if query:
            res = eval(query)
            files = [self._files[index]
                     for index, item in enumerate(list(res))
                     if item == 1]
            return files
