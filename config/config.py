import json


class Config():
    """This is a simple class to read configuration data from the config.json
    file and store it here.

    """

    def __init__(self):
        """Initialization of the Config.

        _config: A dictionary used to hold the configuration read from the
        'config.json' file.

        """
        with open('config.json') as config_file:
            self._config = json.load(config_file)

    def remove_stopwords(self):
        """This function returns whether the program should remove stopwords or
        no, based on the configuration file. If the configuration file is not
        present or the parameter 'remove_stop_words' is missing, it defaults to
        True.

        Returns:
            True if stopwords should be removed, False otherwise.

        """
        return self._config.get('remove_stop_words', True)

    def language(self):
        """This function returns the language used for stop word removal.
        Defaults to english if the parameter is missing.

        Returns:
            The language used for stopwords removal.

        """
        return self._config.get('stop_words_language', 'english')

    def use_stemming(self):
        """This function returns whether the program should use stemming.

        Returns:
            True if stemming should be used, False otherwise.

        """
        # If 'remove_stop_words' is set to true and language is not english,
        # don't apply stemming
        if self.remove_stopwords() and self.language() != 'english':
            return False
        return self._config.get('use_stemming', False)
