from model import Index

import json
import unittest
import unittest.mock as mock
from collections import defaultdict

class IndexTestCase(unittest.TestCase):

    @mock.patch('model.index.Config.__init__', autospec=True, spec_set=True)
    def test_index_raises_value_error_when_wrong_config_file(self, mock_config):
        mock_config.side_effect = ValueError
        with self.assertRaises(ValueError):
            index = Index()

    def test_add_file_raises_index_error(self):
        with mock.patch('model.index.Config', autospec=True, spec_set=True):
            with mock.patch('builtins.open', mock.mock_open()):
                index = Index()
                index.add_file('doc1')
                with self.assertRaises(IndexError):
                    index.add_file('doc1')


    def test_add_file_raises_file_not_found_error(self):
        with mock.patch('model.index.Config', autospec=True, spec_set=True):
            with mock.patch('builtins.open', mock.mock_open()) as m:
                m.side_effect = FileNotFoundError
                index = Index()
                with self.assertRaises(FileNotFoundError):
                    index.add_file('doc1')

    def test_add_file_raises_is_a_directory_error(self):
        with mock.patch('model.index.Config', autospec=True, spec_set=True):
            with mock.patch('builtins.open', mock.mock_open()) as m:
                m.side_effect = IsADirectoryError
                index = Index()
                with self.assertRaises(IsADirectoryError):
                    index.add_file('doc1')

    def test_add_file_raises_permission_error(self):
        with mock.patch('model.index.Config', autospec=True, spec_set=True):
            with mock.patch('builtins.open', mock.mock_open()) as m:
                m.side_effect = PermissionError
                index = Index()
                with self.assertRaises(PermissionError):
                    index.add_file('doc1')

    def test_add_file_correct_input_with_more_files(self):
        with mock.patch('model.index.Config', autospec=True, spec_set=True):
            with mock.patch('builtins.open', mock.mock_open()) as m:
                index = Index()
                index.add_file('doc1')
                index.add_file('doc2')
                index.add_file('doc3')
                with self.assertRaises(IndexError):
                    index.add_file('doc3')
            assert index._files == ['doc1', 'doc2', 'doc3']

    def test_add_file_correct_input_one_file(self):
        with mock.patch('model.index.Config', autospec=True, spec_set=True):
            with mock.patch('builtins.open', mock.mock_open()) as m:
                index = Index()
                index.add_file('document')
            m.assert_called_once_with('document')


    def test_add_file_correct_index_structure_with_more_files(self):
        data1 = 'some data'
        data2 = 'data here'
        expected = {'some': [1], 'data': [1, 2], 'here': [2]}
        with mock.patch('model.index.Config', autospec=True, spec_set=True) as mock_config:
            mock_config.return_value.remove_stopwords.return_value = False
            mock_config.return_value.language.return_value = 'english'
            mock_config.return_value.use_stemming.return_value = False
            index = Index()
            with mock.patch('builtins.open', mock.mock_open(read_data=data1)) as m:
                index.add_file('document1')
            with mock.patch('builtins.open', mock.mock_open(read_data=data2)) as m:
                index.add_file('document2')
            assert index._index == expected


    def test_index_structure_with_stemming_enabled(self):
        data = 'cycling continuos continue'
        expected = {'cycl': [1], 'continuo': [1], 'continu': [1]}
        with mock.patch('model.index.Config', autospec=True, spec_set=True) as mock_config:
            mock_config.return_value.remove_stopwords.return_value = False
            mock_config.return_value.language.return_value = 'english'
            mock_config.return_value.use_stemming.return_value = True
            with mock.patch('builtins.open', mock.mock_open(read_data=data)):
                index = Index()
                index.add_file('doc1')
            assert index._index == expected

    def test_index_structure_with_stemming_disabled(self):
        data = 'cycling continuos continue'
        expected = {'cycling': [1], 'continuos': [1], 'continue': [1]}
        with mock.patch('model.index.Config', autospec=True, spec_set=True) as mock_config:
            mock_config.return_value.remove_stopwords.return_value = False
            mock_config.return_value.language.return_value = 'english'
            mock_config.return_value.use_stemming.return_value = False
            with mock.patch('builtins.open', mock.mock_open(read_data=data)):
                index = Index()
                index.add_file('doc1')
            assert index._index == expected

    def test_add_file_with_identic_words(self):
        data = 'data data data'
        expected = {'data': [1]}
        with mock.patch('model.index.Config', autospec=True, spec_set=True) as mock_config:
            mock_config.return_value.remove_stopwords.return_value = False
            mock_config.return_value.language.return_value = 'english'
            mock_config.return_value.use_stemming.return_value = False
            with mock.patch('builtins.open', mock.mock_open(read_data=data)) as m:
                index = Index()
                index.add_file('doc1')
            assert index._index == expected

    def test_add_file_with_remove_stop_word_enabled(self):
        data = 'at some I am here before as so me'
        expected = defaultdict(list, {'some': [1], 'here': [1], 'before': [1]})
        with mock.patch('model.index.Config', autospec=True, spec_set=True) as mock_config:
            mock_config.return_value.remove_stopwords.return_value = True
            mock_config.return_value.language.return_value = 'english'
            mock_config.return_value.use_stemming.return_value = False
            with mock.patch('builtins.open', mock.mock_open(read_data=data)) as m:
                index = Index()
                index.add_file('doc1')
            assert index._index == expected

    def test_add_file_with_wrong_type(self):
        with mock.patch('model.index.Config', autospec=True, spec_set=True) as mock_config:
            mock_config.return_value.remove_stopwords.return_value = False
            mock_config.return_value.language.return_value = 'english'
            mock_config.return_value.use_stemming.return_value = False
            with mock.patch('builtins.open', mock.mock_open()) as m:
                index = Index()
                with self.assertRaises(ValueError):
                    index.add_file(None)
                with self.assertRaises(ValueError):
                    index.add_file([])
                with self.assertRaises(ValueError):
                    index.add_file(True)
                with self.assertRaises(ValueError):
                    index.add_file({})

    def test_add_file_with_empty_file_name(self):
        with mock.patch('model.index.Config', autospec=True, spec_set=True) as mock_config:
            mock_config.return_value.remove_stopwords.return_value = False
            mock_config.return_value.language.return_value = 'english'
            mock_config.return_value.use_stemming.return_value = False
            with mock.patch('builtins.open', mock.mock_open()) as m:
                m.side_effect = FileNotFoundError
                index = Index()
                with self.assertRaises(FileNotFoundError):
                    index.add_file('')

    def test_add_file_with_stop_words_and_stemming_enabled(self):
        data = 'this is some data that needs stemming ;continue hello world'
        expected = defaultdict(list, {'this': [1], 'some': [1], 'data': [1], 'that': [1], 'need': [1], 'stem': [1], 'continu': [1], 'hello': [1], 'world': [1]})
        with mock.patch('model.index.Config', autospec=True, spec_set=True) as mock_config:
            mock_config.return_value.remove_stopwords.return_value = True
            mock_config.return_value.language.return_value = 'english'
            mock_config.return_value.use_stemming.return_value = True
            with mock.patch('builtins.open', mock.mock_open(read_data=data)) as m:
                index = Index()
                index.add_file('doc1')
            assert index._index == expected

    def test_good_query_with_words_in_index(self):
        index = defaultdict(list, {'data': [1, 3], 'some':[1, 2], 'hello': [1], 'world': [3]})
        files = ['doc1', 'doc2', 'doc3', 'doc4']
        query = 'data && some && (hello || world)'
        expected = ['doc1']
        with mock.patch('model.index.Config', autospec=True, spec_set=True) as mock_config:
            mock_config.return_value.remove_stopwords.return_value = False
            mock_config.return_value.language.return_value = 'english'
            mock_config.return_value.use_stemming.return_value = False
            idx = Index()
            idx._index = index
            idx._files = files
            assert idx.get_result_for_query(query) == expected

    def test_good_query_with_words_not_in_index(self):
        index = defaultdict(list, {'data': [1, 3], 'some':[1, 2], 'hello': [1], 'world': [3]})
        files = ['doc1', 'doc2', 'doc3', 'doc4']
        query = 'this && is && (not || ok)'
        expected = []
        with mock.patch('model.index.Config', autospec=True, spec_set=True) as mock_config:
            mock_config.return_value.remove_stopwords.return_value = False
            mock_config.return_value.language.return_value = 'english'
            mock_config.return_value.use_stemming.return_value = False
            idx = Index()
            idx._index = index
            idx._files = files
            assert idx.get_result_for_query(query) == expected


    def test_empty_query(self):
        index = defaultdict(list, {'data': [1, 3], 'some':[1, 2], 'hello': [1], 'world': [3]})
        files = ['doc1', 'doc2', 'doc3', 'doc4']
        query = ''
        expected = None
        with mock.patch('model.index.Config', autospec=True, spec_set=True) as mock_config:
            mock_config.return_value.remove_stopwords.return_value = False
            mock_config.return_value.language.return_value = 'english'
            mock_config.return_value.use_stemming.return_value = False
            idx = Index()
            idx._index = index
            idx._files = files
            assert idx.get_result_for_query(query) == expected

    def test_wrong_query(self):
        index = defaultdict(list, {'data': [1, 3], 'some':[1, 2], 'hello': [1], 'world': [3]})
        files = ['doc1', 'doc2', 'doc3', 'doc4']
        query = 'data. some hello this is wrong query !'
        with mock.patch('model.index.Config', autospec=True, spec_set=True) as mock_config:
            mock_config.return_value.remove_stopwords.return_value = False
            mock_config.return_value.language.return_value = 'english'
            mock_config.return_value.use_stemming.return_value = False
            idx = Index()
            idx._index = index
            idx._files = files
            with self.assertRaises(ValueError):
                result = idx.get_result_for_query(query)
