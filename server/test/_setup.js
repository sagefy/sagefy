require('../index')

module.exports = async () => {
  // Postgraphile needs some time to generate the schemas,
  // otherwise the whole thing fails at the end.
  return new Promise(resolve => setTimeout(resolve, 2000))
}
