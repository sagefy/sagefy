module.exports = function valuefy(value) {
  if (typeof value === 'undefined') return undefined
  if (value === 'true') return true
  if (value === 'false') return false
  if (value === 'null') return null
  if (value.match(/^\d+\.\d+$/)) return parseFloat(value)
  if (value.match(/^\d+$/)) return parseInt(value, 10)
  return decodeURIComponent(value)
}
