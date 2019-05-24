module.exports = function shorten(str, maxLen = 200, separator = ' ') {
  // https://stackoverflow.com/a/5454303/1509526
  let s = str.replace(/\n+/g, ' ').substr(0, maxLen)
  s = s.substr(0, Math.min(s.length, s.lastIndexOf(separator)))
  if (s.length < str.length) s += '...'
  return s
}
