const { pool } = require('../index')

module.exports = async () => pool.end()
