# Read, create, update, and delete cookies.

encode = encodeURIComponent
decode = decodeURIComponent

# Read and parse a cookie key/value.
read = (s) ->
    if s.indexOf('"') is 0
        s = s.slice(1, -1).replace(/\\"/g, '"').replace(/\\\\/g, '\\')
    return decode(s.replace(/\+/g, ' '))

# Get the cookie value at a particular key.
get = (key) ->
    name = key + '='
    cookies = document.cookie.split(';')
    for c in cookies
        c = c.trim()
        if c.indexOf(name) is 0
            return read(c.substring(name.length))
    return null

# Set the cookie value at a specific key.
set = (key, value, time = 31556926) ->
    return document.cookie = [
        encode(key), '=', ('' + value),
        ';path=/',
        ";max-age=#{time}"
    ].join('')

# Remove the cookie value at a specific key.
unset = (key) ->
    return set(key, '', -1)

module.exports = {
    read
    get
    set
    unset
}
