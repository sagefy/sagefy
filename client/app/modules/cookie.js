// Read, create, update, and delete cookies.
const encode = encodeURIComponent
const decode = decodeURIComponent

// Read and parse a cookie key/value.
const read = (s) => {
    if (s.indexOf('"') === 0) {
        s = s.slice(1, -1).replace(/\\"/g, '"').replace(/\\\\/g, '\\')
    }
    return decode(s.replace(/\+/g, ' '))
}

// Get the cookie value at a particular key.
const get = (key) => {
    if (typeof document === 'undefined') { return null }
    const name = `${key}=`
    const cookies = document.cookie.split(';')
    for (let c of cookies) {
        c = c.trim()
        if (c.indexOf(name) === 0) {
            return read(c.substring(name.length))
        }
    }
    return null
}

// Set the cookie value at a specific key.
const set = (key, value, time = 31556926) => {
    if (typeof document === 'undefined') { return }
    if (value === null || value === undefined) { return }
    document.cookie = [
        encode(key), '=', `${value}`,
        ';path=/',
        `;max-age=${time}`,
    ].join('')
    return document.cookie
}

// Remove the cookie value at a specific key.
const unset = (key) => {
    return set(key, '', -1)
}

module.exports = {
    read,
    get,
    set,
    unset,
}
