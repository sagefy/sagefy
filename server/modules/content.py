"""
Makes content in /content in YAML format available to the Python code.
"""

import os
import yaml

files = {}


def get(key, language='en'):
    """
    Given a filename, key and language, get the matching content.
    """

    if language not in files:
        try:
            path = '/content/%s.yml' % (language,)
            if os.environ.get('TRAVIS'):
                path = '../content/%s.yml' % (language,)
            stream = open(path, 'r')
            files[language] = yaml.load(stream)[language]
            stream.close()
        except:
            files[language] = files['en']
    s = files[language][key]
    assert s, "Not Found > {lang} @ {key}".format(lang=language, key=key)
    return s
