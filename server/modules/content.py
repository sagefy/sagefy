"""
Makes content in ../content in YAML format available to the Python code.
"""


import yaml
import os

files = {}

dirname = os.path.realpath(__file__).replace('/server/modules/content.py', '')


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
