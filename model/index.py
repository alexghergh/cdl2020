from model.list import IndexList

from config import config
from collections import defaultdict
import re


class Index():
    """This class is meant to hold information about the index.

    The way we hold an index is through these 2 fields:
      1. files: A list keeping the names of the files scanned so far.
      2. index: A dictionary that holds words as keys, and the files' number
      they appear in as values. The values are lists of integers representing
      the files a word appears in.

    """

    def __init__(self):
        """Initialization of the index.

        _files: Initialize the files to an empty list.

        _index: The index has a structure like this:
            {
                'from': [1, 2],
                'kernel': [1],
                'c': [2, 3],
            }
        where 'from', 'kernel' and 'c' are words from the documents.

        _regex: A regex expression to match words only, since that is what
        we're interested in.

        _config: A Config instance through which the Index receives certain
        configs from the external file 'config.json'.
        For more see config/config.py.

        """
        self._files = []
        self._index = defaultdict(list)
        self._regex = re.compile(r'\w+')
        self._config = config

    def add_file(self, file_name):
        """Scan a file and add the words to the index.

        Args:
            file_name: The file to be scanned.

        Returns:
            Success string if the file was added to index.

        Raises:
            IndexError: If the file is already in the index.
            FileNotFoundError: If the file does not exist.
            IsADirectoryError: If a directory was passed.
            PermissionError: If the user running the script doesn't have
                permission on a file.
            Exception: If another exception arose.

        """
        # Return if file was already scanned
        if file_name in self._files:
            raise IndexError(f'[Error] "{file_name}" is already in the index!')

        try:

            with open(file_name) as file:
                # Add the file name to the files list
                self._files.append(file_name)

                # Construct a set from the words within the file
                words = set(self._regex.findall(file.read().lower()))

                # If 'remove_stopwords' is set, remove the stopwords
                if self._config.remove_stopwords():
                    words = self._remove_stopwords(words)

                # Add the words to the index
                for word in words:
                    self._index[word].append(len(self._files))

        except FileNotFoundError:
            raise FileNotFoundError(f'[Error] The file "{file_name}" does not exist!')
        except IsADirectoryError:
            raise IsADirectoryError(f'[Error] "{file_name}" is a directory!')
        except PermissionError:
            raise PermissionError(f'[Error] Permission denied for "{file_name}"!')
        except Exception as e:
            raise Exception(f'An error occured for "{file_name}": ', e)
        else:
            return f'[Success] The file "{file_name}" was added to index!'

    def get_result_for_query(self, query):
        """This function returns a result for a query.

        Args:
            query: The query to return a result for.
            A query has the form of:
            - word1 && word2 || (word3 && !word4)
            It can have any variations of words and signs.

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

    def _remove_stopwords(self, words_list):
        """This function uses the stopwords directory to remove stopwords from
        a list of words.

        Stopwords are words that do not carry information, i.e. they are useless
        in the context of a search engine ('a', 'is', 'any', 'before', etc.).

        Args:
            words_list: The word list that needs to be picked for stopwords.

        """
        with open(f'stopwords/{self._config.language()}') as stopwords_file:
            stop_words = [x.strip() for x in stopwords_file.readlines()]

        return [word for word in words_list if word not in stop_words and
                len(word) > 2]

    def _get_index_list_for_word(self, word):
        """This function returns an IndexList associated with a word.

        Example:
            A word goes from [1, 2, 5] in the index to [1, 1, 0, 0, 1] in order
            to create an IndexList from it.

        For more info see IndexList in 'list.py'.

        Args:
            word: The word to return an IndexList for.

        """
        # Populate the lists with 0's
        word_list = [0] * len(self._files)

        # Change it to 1 when the word appears in a file
        for item in self._index[word.lower()]:
            word_list[item - 1] = 1
        return IndexList(word_list)
