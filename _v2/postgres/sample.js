/* eslint-disable security/detect-object-injection, import/no-extraneous-dependencies, no-console */

const fs = require('fs').promises
const yaml = require('js-yaml')
const { Client } = require('pg')

require('dotenv').config()

const userData = [
  {
    name: 'Addi',
    email: 'addi@example.com',
    password: 'addiexamplepassword',
    role: 'sg_admin',
    viewSubjects: true,
    emailFrequency: 'immediate',
  },
  {
    name: 'Ursa',
    email: 'ursa@example.com',
    password: 'ursaexamplepassword',
    role: 'sg_user',
    viewSubjects: true,
    emailFrequency: 'daily',
  },
  {
    name: 'Umeko',
    email: 'umeko@example.com',
    password: 'umekoexamplepassword',
    role: 'sg_user',
    viewSubjects: false,
    emailFrequency: 'never',
  },
]

function ucfirst(s) {
  if (typeof s !== 'string') return ''
  return s.charAt(0).toUpperCase() + s.slice(1)
}

async function connectToDatabase() {
  const client = new Client()
  return client.connect({
    // user
    // host
    // database
    // password
    // port
  })
}

async function emptyDatabase(db) {
  await db.query('drop database if exists sagefy')
  await db.query('create database sagefy')
}

async function writeDatabaseSchema(db) {
  const sql = await fs.readFile('sample.sql', 'utf8')
  return db.query(sql)
}

async function readYaml() {
  return yaml.safeLoad(await fs.readFile('sample.yml', 'utf8'))
}

async function makeUsers(db) {
  // Anonymous user name: Anora
  return Promise.all(
    userData.map(
      async ({
        name,
        email,
        password,
        role,
        viewSubjects,
        emailFrequency,
      }) => {
        const user = await db.query(`select sg_public.sign_up($1, $2, $3)`, [
          name,
          email,
          password,
        ])
        await db.query(
          `
      update sg_private.user
      set role = $2, email_frequency = $3
      where user_id = $1;
    `,
          [user.id, role, emailFrequency]
        )
        await db.query(
          `
      update sg_public.user
      set view_subjects = $2
      where id = $1
    `,
          [user.id, viewSubjects]
        )
        return user
      }
    )
  )
}

async function makeUnits({ db, lookUp, sample }) {
  // TODO pass in a user...?
  return Promise.all(
    Object.entries(sample.units).map(
      async ([sampleId, { name, body, require_ids: requireIds }]) => {
        requireIds = requireIds.map(s => lookUp[s])
        const unit = db.query(
          `select sg_public.new_unit($1, $2, $3, $4, $5)`,
          ['en', name, [], body, requireIds]
        )
        lookUp[sampleId] = unit.entity_id
        return unit
      }
    )
  )
}

async function makeSubjects({ db, lookUp, sample }) {
  // TODO pass in a user...?
  return Promise.all(
    Object.entries(sample.subjects).map(
      async ([sampleId, { name, body, members }]) => {
        const membersMapped = members.map(({ kind, id }) => ({
          kind,
          id: lookUp[id],
        }))
        const subject = db.query(
          `select sg_public.new_subject($1, $2, $3, $4, $5)`,
          ['en', name, [], body, membersMapped]
        )
        lookUp[sampleId] = subject.entity_id
        return subject
      }
    )
  )
}

async function makeCards({ db, lookUp, sample, units }) {
  // TODO pass in a user...?
  return Promise.all(
    Object.entries(sample.cards).map(([kind, cards]) =>
      Promise.all(
        cards.map(({ name, unit, ...data }) => {
          const unitId = lookUp[unit]
          const fullUnit = units.findOne(u => u.id === unitId)
          return db.query(
            `create function sg_public.new_card($1, $2, $3, $4, $5, $6)`,
            [
              'en',
              name || data.body || `${ucfirst(kind)}: ${fullUnit.name}`,
              [],
              unitId,
              kind,
              data,
            ]
          )
        })
      )
    )
  )
}

async function makeTopicsAndPosts({ db, lookUp, sample, users }) {}

async function makeFollowsAndNotices({ db, lookUp, sample, users }) {}

async function makeUserSubjectsAndResponses({ db, lookUp, sample, users }) {}

async function makeSuggests({ db, lookUp, sample, users }) {}

async function makeSample() {
  if (env === 'PRODUCTION') {
    throw new Error('You must be in test or development to wipe the database.')
  }
  const sample = await readYaml()
  const db = await connectToDatabase()
  await emptyDatabase(db)
  await writeDatabaseSchema(db)
  const users = await makeUsers(db)
  const lookUp = {}
  const units = await makeUnits({ db, lookUp, sample })
  await makeSubjects({ db, lookUp, sample })
  await makeCards({ db, lookUp, sample, units })
  const { topics, posts } = await makeTopicsAndPosts({
    db,
    lookUp,
    sample,
    users,
  })
  const { follows, notices } = await makeFollowsAndNotices({
    db,
    lookUp,
    sample,
    users,
  })
  const { userSubjects, responses } = await makeUserSubjectsAndResponses({
    db,
    lookUp,
    sample,
    users,
  })
  const { suggests, suggestFollows } = await makeSuggests({
    db,
    lookUp,
    sample,
    users,
  })
  await db.end()
}

if (require.main === module) {
  try {
    console.log('Resetting database to sample.')
    makeSample()
    console.log('Finished resetting the database.')
  } catch (e) {
    console.error(e)
  }
}
