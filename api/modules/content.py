"""
Makes content in ../content in YAML format available to the Python API.
"""


import yaml
import os
from modules.util import get_first

files = {}

dirname = os.path.dirname(__file__).replace('/api/modules', '')


def get(key, language='en'):
    """
    Given a filename, key and language, get the matching content.
    """
    if language not in files:
        stream = open('%s/content/%s.yml' % (dirname, language), 'r')
        files[language] = yaml.load(stream)[language]
        stream.close()

    s = files[language][key]
    assert s, "Not Found > {lang} @ {key}".format(lang=language,
                                                  key=key)
    return s
