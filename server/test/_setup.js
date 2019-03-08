require('../index')

// So the story here is that postgraphile needs some time to generate the
// schemas, otherwise the whole thing fails at the end.

module.exports = async () => new Promise(resolve => setTimeout(resolve, 2000))
