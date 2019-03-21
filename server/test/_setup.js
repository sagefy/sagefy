require('../index')
const generateDevData = require('./_dev-data')

module.exports = async () => {
  await generateDevData()
  // Postgraphile needs some time to generate the schemas,
  // otherwise the whole thing fails at the end.
  return new Promise(resolve => setTimeout(resolve, 2000))
}
