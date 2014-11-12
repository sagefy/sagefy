files = {}
files.error = require('../content/error.json')
files.form = require('../content/form.json')
files.user = require('../content/user.json')

# Given a filename, a key, and the language,
# provide the appropriate content.
# TODO: Update so default to lang, then default to `en`
get = (filename, key, language = 'en') ->
    return files[filename][key][language]

module.exports = {get: get}
