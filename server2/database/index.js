/*
Ordering functions for this directory:

get
list
insert
update
delete

simple -> complex
high -> low
general -> specific

*/

const { Pool } = require('pg')

const pool = new Pool()

module.exports = {
  query(text, params) {
    return pool.query(text, params)
  },
}
