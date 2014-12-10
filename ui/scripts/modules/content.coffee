files = {}
files.error = require('../content/error.json')
files.form = require('../content/form.json')
files.user = require('../content/user.json')

# Given a filename, a key, and the language,
# provide the appropriate content.
get = (filename, key, language = 'en') ->
    k = files[filename][key]
    for lang in [language, language[..1], 'en']
        if k[lang]
            return k[lang]

module.exports = {get: get}
