"""
Makes content in /content in YAML format available to the Python code.
"""

import os
import yaml

FILES = {}


def get(key, language='en'):
  """
  Given a filename, key and language, get the matching content.
  """

  if language not in FILES:
    try:
      path = '/content/%s.yml' % (language,)
      if os.environ.get('TRAVIS'):
        path = '../content/%s.yml' % (language,)
      stream = open(path, 'r')
      FILES[language] = yaml.load(stream)[language]
      stream.close()
    except:
      FILES[language] = FILES['en']
  content_string = FILES[language][key]
  assert content_string, "Not Found > {lang} @ {key}".format(lang=language, key=key)
  return content_string
