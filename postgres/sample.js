/* eslint-disable import/no-extraneous-dependencies */

const yaml = require('js-yaml')
const fs = require('fs').promises
const { Client } = require('pg')

async function main() {
  const db = new Client({
    user: 'sagefy',
    host: 'localhost',
    port: '5432',
    database: 'sagefy',
  })
  await db.connect()
  await db.query(`
    SELECT set_config(
      'jwt.claims.session_id',
      '3b336a03-c313-4a21-af1e-da0a83c813ea',
      false
    );
  `)

  const sampleSuggests = yaml.safeLoad(
    await fs.readFile('./sample-suggests.yaml', 'utf8')
  )
  await Promise.all(
    sampleSuggests.map(async ({ name, body }) =>
      db.query(
        `
        insert into sg_public.suggest (name, body)
        values ($1, $2)
      `,
        [name, body]
      )
    )
  )

  await db.end()
}

if (require.main === module) {
  main()
}
