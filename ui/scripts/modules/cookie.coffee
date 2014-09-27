_ = require('../framework/utilities')
cookie = {}

cookie.encode = (s) -> return encodeURIComponent(s)
cookie.decode = (s) -> return decodeURIComponent(s)
cookie.stringify = (s) -> return '' + s

cookie.read = (s) ->
    if s.indexOf('"') is 0
        s = s.slice(1, -1).replace(/\\"/g, '"').replace(/\\\\/g, '\\')
    return cookie.decode(s.replace(/\+/g, ' '))

cookie.get = (key) ->
    name = key + '='
    cookies = document.cookie.split(';')
    for c in cookies
        c = c.trim()
        if c.indexOf(name) is 0
            return cookie.read(c.substring(name.length))
    return null

cookie.set = (key, value, time = 31556926) ->
    return document.cookie = [
        cookie.encode(key), '=', cookie.stringify(value), '; ',
        'path=/; ',
        "max-age=#{time}; "
    ].join('')

cookie.unset = (key) ->
    return cookie.set(key, '', -1)

module.exports = cookie
