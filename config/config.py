import json
import warnings
import os


class Config():
    """This is a simple class to read configuration data from the config.json
    file and store it here.

    """

    def __init__(self):
        """Initialization of the Config.

        _config: A dictionary used to hold the configuration read from the
        'config.json' file.

        Raises:
            ValueError: if the config.json has wrong format.

        """
        try:

            with open('config.json') as config_file:
                self._config = json.load(config_file)

        except FileNotFoundError:
            warnings.warn('[Warning] Could not find config.json. Continuing with defaults.')
            self._config = {}
        except json.decoder.JSONDecodeError as e:
            raise json.decoder.JSONDecodeError('[JSON Error] Please check that your config.json file is correct.', e.doc, e.pos)

    def remove_stopwords(self):
        """This function returns whether the program should remove stopwords or
        no, based on the configuration file. If the configuration file is not
        present or the parameter 'remove_stop_words' is missing, it defaults to
        True.

        Returns:
            True if stopwords should be removed, False otherwise.

        """
        remove_stopwords = self._config.get('remove_stop_words', False)
        if remove_stopwords not in [False, True]:
            return False
        return remove_stopwords

    def language(self):
        """This function returns the language used for stop word removal.
        Defaults to english if the parameter is missing.

        Returns:
            The language used for stopwords removal.

        """
        language = self._config.get('stop_words_language', 'english')
        if language not in os.listdir('stopwords'):
            warnings.warn(f"[Warning] Language '{language}' not supported, continuing with english.")
            return 'english'
        return language

    def use_stemming(self):
        """This function returns whether the program should use stemming.

        Returns:
            True if stemming should be used, False otherwise.

        """
        use_stemming = self._config.get('use_stemming', False)
        if use_stemming not in [False, True]:
            return False
        # If 'remove_stop_words' is set to true and language is not english,
        # don't apply stemming
        if self.remove_stopwords() and self.language() != 'english':
            return False
        return use_stemming
