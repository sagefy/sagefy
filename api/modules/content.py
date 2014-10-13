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

_ = get
