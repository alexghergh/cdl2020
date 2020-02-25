from config import Config

import unittest
import unittest.mock as mock

class ConfigTestCase(unittest.TestCase):

    def test_remove_stopwords_does_not_exist_in_config(self):
        data = '{}'
        with mock.patch('builtins.open', mock.mock_open(read_data=data)):
            config = Config()
            assert config.remove_stopwords() == False

    def test_remove_stopwords_in_config_is_true(self):
        data = '{"remove_stop_words": true}'
        with mock.patch('builtins.open', mock.mock_open(read_data=data)):
            config = Config()
            assert config.remove_stopwords() == True

    def test_remove_stopwords_in_config_is_false(self):
        data = '{"remove_stop_words": false}'
        with mock.patch('builtins.open', mock.mock_open(read_data=data)):
            config = Config()
            assert config.remove_stopwords() == False

    def test_remove_has_wrong_attribute_in_config(self):
        data = '{"remove_stop_words": "whatever"}'
        with mock.patch('builtins.open', mock.mock_open(read_data=data)):
            config = Config()
            assert config.remove_stopwords() == False

    def test_language_has_supported_language(self):
        data = '{"stop_words_language": "romanian"}'
        with mock.patch('builtins.open', mock.mock_open(read_data=data)):
            config = Config()
            assert config.language() == 'romanian'

    def test_language_does_not_exist_in_config(self):
        data = '{}'
        with mock.patch('builtins.open', mock.mock_open(read_data=data)):
            config = Config()
            assert config.language() == 'english'

    def test_language_in_config_is_true(self):
        data = '{"stop_words_language": true}'
        with mock.patch('builtins.open', mock.mock_open(read_data=data)):
            config = Config()
            with self.assertWarns(UserWarning):
                assert config.language() == 'english'

    def test_language_in_config_is_false(self):
        data = '{"stop_words_language": false}'
        with mock.patch('builtins.open', mock.mock_open(read_data=data)):
            config = Config()
            with self.assertWarns(UserWarning):
                assert config.language() == 'english'

    def test_language_in_config_does_not_have_language_supported(self):
        data = '{"stop_words_language": "some other language"}'
        with mock.patch('builtins.open', mock.mock_open(read_data=data)):
            config = Config()
            with self.assertWarns(UserWarning):
                assert config.language() == 'english'

    def test_stemming_does_not_exist_in_config(self):
        data = '{}'
        with mock.patch('builtins.open', mock.mock_open(read_data=data)):
            config = Config()
            assert config.use_stemming() == False

    def test_stemming_in_config_is_true(self):
        data = '{"use_stemming": true}'
        with mock.patch('builtins.open', mock.mock_open(read_data=data)):
            config = Config()
            assert config.use_stemming() == True

    def test_stemming_in_config_is_false(self):
        data = '{"use_stemming": false}'
        with mock.patch('builtins.open', mock.mock_open(read_data=data)):
            config = Config()
            assert config.use_stemming() == False


    def test_stemming_disabled_when_remove_stopwords_true_and_language_not_english(self):
        data = '{"remove_stop_words": true,"stop_words_language": "romanian","use_stemming": true}'
        with mock.patch('builtins.open', mock.mock_open(read_data=data)):
            config = Config()
            assert config.use_stemming() == False

    def test_stemming_wrong_attribute_in_config(self):
        data = '{"use_stemming": "whatever"}'
        with mock.patch('builtins.open', mock.mock_open(read_data=data)):
            config = Config()
            assert config.use_stemming() == False

    def test_wrong_json_in_config_file_raise_value_error(self):
        # This JSON has an extra comma at the end
        wrong_data = '{"remove_stop_words": false,"stop_words_language": "english","use_stemming": false,}'
        with mock.patch('builtins.open', mock.mock_open(read_data=wrong_data)):
            with self.assertRaises(ValueError):
                config = Config()

    def test_config_file_does_not_exist_raise_warning(self):
        with mock.patch('builtins.open', mock.mock_open()) as m:
            m.side_effect = FileNotFoundError
            with self.assertWarns(UserWarning):
                config = Config()

    def test_good_config_file(self):
        data = '{"remove_stop_words": true,"stop_words_language": "english","use_stemming": false}'
        with mock.patch('builtins.open', mock.mock_open(read_data=data)) as m:
            config = Config()
            assert config.remove_stopwords() == True
            assert config.language() == 'english'
            assert config.use_stemming() == False
        m.assert_called_once_with('config.json')
