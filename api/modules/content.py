"""
Makes content in ../content in YAML format available to the Python API.
"""


import yaml
import os

files = {}

dirname = os.path.dirname(__file__).replace('/api/modules', '')


def get(filename, key, language='en'):
    """
    Given a filename, key and language, get the matching content.
    """
    if filename not in files:
        stream = open('%s/content/%s.yml' % (dirname, filename), 'r')
        files[filename] = yaml.load(stream)
        stream.close()
    return files[filename][key][language]
    # TODO: Update so default to lang, then default to `en`

_ = get
