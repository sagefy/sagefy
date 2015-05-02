files = {}
files.en = require('../content/en.json')
files.eo = require('../content/eo.json')

# Given a key and the language, provide the appropriate content.
get = (key, language = 'en') ->
    if not files[language]
        return "No Language > #{language}"
    if not files[language][key]
        return "Not Found > #{language} @ #{key}"
    return files[language][key]

module.exports = {get: get}
