// https://stackoverflow.com/a/13653180/1509526
const UUID_REGEXP = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i

module.exports = function isUuid(s) {
  return UUID_REGEXP.test(s)
}
