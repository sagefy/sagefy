/* eslint-disable no-restricted-syntax, no-await-in-loop, import/no-extraneous-dependencies, security/detect-object-injection, camelcase, prefer-destructuring, no-param-reassign, no-console */
const { Client } = require('pg')
const fs = require('fs').promises
const yaml = require('js-yaml')
const uuidv4 = require('uuid/v4')

const TABLES = [
  'sg_public."user"',
  'sg_private."user"',
  'sg_public.entity',
  'sg_public.entity_version',
  'sg_public.subject_entity',
  'sg_public.subject_version',
  'sg_public.subject_version_before_after',
  'sg_public.subject_version_parent_child',
  'sg_public.card_entity',
  'sg_public.card_version',
  // 'sg_public.user_subject',
  // 'sg_public.response',
]

async function makeClient() {
  console.log('Connecting to database...')
  const client = new Client({ connectionString: process.env.DATABASE_URL })
  await client.connect()
  return client
}

async function cleanDatabase(client) {
  console.log('Truncating tables...')
  await client.query(`truncate ${TABLES.reverse().join(', ')} cascade;`)
  return client
}

async function letsJwtIn(client, { role, user_id, session_id, uniq }) {
  // Note that this does not use `local`,
  // so it sticks until called again.
  // TODO use node-pg transactions instead?
  const query = `
    set role ${role};
    ${role ? `set jwt.claims.role to '${role}';` : ''}
    ${user_id ? `set jwt.claims.user_id to '${user_id}';` : ''}
    ${session_id ? `set jwt.claims.session_id to '${session_id}';` : ''}
    ${uniq ? `set jwt.claims.uniq to '${uniq}';` : ''}
  `
  return client.query(query)
}

async function letsJwtOut(client) {
  return client.query(`
    reset role;
    reset jwt.claims.role;
    reset jwt.claims.user_id;
    reset jwt.claims.session_id;
    reset jwt.claims.uniq;
  `)
}

async function newAnon(client) {
  return (await client.query(`select * from sg_public.get_anonymous_token();`))
    .rows[0]
}

async function newUser(client, { name, email, password }) {
  return (await client.query(`select * from sg_public.sign_up($1, $2, $3);`, [
    name,
    email,
    password,
  ])).rows[0]
}

async function newSubject(client, { name, body, parent, before }) {
  return (await client.query(
    `select * from sg_public.new_subject(
      $1, -- language
      $2, -- name
      $3, -- tags
      $4, -- body
      $5, -- parent
      $6  -- before
    );`,
    ['en', name, [], body, parent, before]
  )).rows[0]
}

async function newCard(client, { name, subject_id, kind, data }) {
  return (await client.query(
    `select * from sg_public.new_card(
      $1, -- language
      $2, -- name
      $3, -- tags
      $4, -- subject_id
      $5::sg_public.card_kind, -- kind
      $6  -- data
    )`,
    ['en', name, [], subject_id, kind, JSON.stringify(data)]
  )).rows[0]
}

async function newUserSubject(client, { subject_id }) {
  return (await client.query(
    `insert into sg_public.user_subject
    (subject_id) values ($1)
    returning *;`,
    [subject_id]
  )).rows[0]
}

async function newResponse(client, { card }) {
  const response = (await client.query(`insert into sg_public.response
    (card_id, response)
    values
    ('${card.entity_id}', '${
    Object.entries(card.data.options)
      .filter(([, opt]) => opt.correct)
      .map(([key]) => key)[0]
  }');
    `)).rows[0]
  return response
}

async function makeUsers(client) {
  console.log('Making users...')
  // Ivy: anonymous
  // Jasmine: new/learner
  // Doris: established/contributor
  // Esther: admin
  const ivy = await newAnon(client)
  const jasmine = await newUser(client, {
    name: 'Jasmine',
    email: 'jasmine@example.com',
    password: 'example1',
  })
  const doris = await newUser(client, {
    name: 'Doris',
    email: 'doris@example.com',
    password: 'example1',
  })
  const esther = await newUser(client, {
    name: 'Esther',
    email: 'esther@example.com',
    password: 'example1',
  })
  return { ivy, jasmine, doris, esther }
}

async function makeSubjects(client, { users }) {
  console.log('Creating subjects...')
  await letsJwtIn(client, users.doris)
  const subjects = {}
  const emusYaml = yaml.safeLoad(
    await fs.readFile('./sample-subject.yaml', 'utf8')
  )
  for (const [key, { name, body, parent, before }] of Object.entries(
    emusYaml.subjects
  )) {
    subjects[key] = await newSubject(client, {
      name,
      body,
      parent: parent ? [subjects[parent].entity_id] : [],
      before: before ? before.map(slug => subjects[slug].entity_id) : [],
    })
  }
  const sugYaml = yaml.safeLoad(
    await fs.readFile('./sample-subjects.yaml', 'utf8')
  )
  for (const { name, body } of sugYaml) {
    subjects[name] = await newSubject(client, {
      name,
      body,
      parent: [],
      before: [],
    })
  }
  await letsJwtOut(client)
  await client.query(
    `update sg_public.subject_version set status = 'accepted';`
  )
  return subjects
}

async function makeCards(client, { users, subjects }) {
  console.log('Making cards...')
  const emusYaml = yaml.safeLoad(
    await fs.readFile('./sample-subject.yaml', 'utf8')
  )
  await letsJwtIn(client, users.doris)
  const cards = {
    video: {},
    unscoredEmbed: {},
    page: {},
    choice: {},
  }
  await Promise.all([
    ...emusYaml.cards.video.map(async ({ subject, video_id }) => {
      cards.video[subject] = await newCard(client, {
        name: `Video: ${subjects[subject].name}`,
        subject_id: subjects[subject].entity_id,
        kind: 'video',
        data: { video_id, site: 'youtube' },
      })
      return cards.video[subject]
    }),
    ...emusYaml.cards.unscored_embed.map(async ({ subject, name, url }) => {
      const card = await newCard(client, {
        name,
        subject_id: subjects[subject].entity_id,
        kind: 'unscored_embed',
        data: { url },
      })
      cards.unscoredEmbed[subject] = cards.unscoredEmbed[subject] || []
      cards.unscoredEmbed[subject].push(card)
      return card
    }),
    ...emusYaml.cards.page.map(async ({ subject, name, body }) => {
      cards.page[subject] = await newCard(client, {
        name,
        subject_id: subjects[subject].entity_id,
        kind: 'page',
        data: { body },
      })
      return cards.page[subject]
    }),
    ...emusYaml.cards.choice.map(async ({ subject, body, options }) => {
      const card = await newCard(client, {
        name: body,
        subject_id: subjects[subject].entity_id,
        kind: 'choice',
        data: {
          body,
          options: options.reduce((sum, { value, correct, feedback }) => {
            sum[uuidv4()] = {
              value,
              feedback,
              correct: correct === 'Y',
            }
            return sum
          }, {}),
          max_options_to_show: 4,
        },
      })
      cards.choice[subject] = cards.choice[subject] || []
      cards.choice[subject].push(card)
      return card
    }),
  ])
  await letsJwtOut(client)
  await client.query(`update sg_public.card_version set status = 'accepted';`)
  return cards
}

async function makeUserSubjects(client, { users, subjects }) {
  console.log('Making user-subjects...')
  const userSubjects = {}
  await letsJwtIn(client, users.doris)
  userSubjects.doris = await newUserSubject(client, {
    subject_id: subjects.all.entity_id,
  })
  await letsJwtIn(client, users.esther)
  userSubjects.esther = await newUserSubject(client, {
    subject_id: subjects.foundation.entity_id,
  })
  await letsJwtOut(client)
  return userSubjects
}

async function makeResponses(client, { users, cards }) {
  console.log('Making responses...')
  await letsJwtIn(client, users.doris)
  const responses = {}
  const subjectsToHit = ['intro', 'params', 'human', 'digital', 'complex']
  for (const subj of subjectsToHit) {
    const card = cards.choice[subj][0]
    responses[subj] = await newResponse(client, { card })
  }
  await letsJwtOut(client)
  await client.query(`
    update sg_public.response set learned = 0.999;
  `)
  return responses
}

async function generateDevData() {
  if (process.env.NODE_ENV === 'production') {
    console.log('I will not run on production.')
    return {}
  }
  console.log('Generating development data...')
  const data = {
    users: {},
    subjects: {},
    cards: {},
    userSubjects: {},
    responses: {},
  }
  const client = await makeClient()
  await cleanDatabase(client)
  Object.assign(data.users, await makeUsers(client, data))
  Object.assign(data.subjects, await makeSubjects(client, data))
  Object.assign(data.cards, await makeCards(client, data))
  Object.assign(data.userSubjects, await makeUserSubjects(client, data))
  Object.assign(data.responses, await makeResponses(client, data))
  await letsJwtOut(client)
  console.log('Finished generating development data.')
  return data
}

if (require.main === module) {
  generateDevData()
    .catch(console.error)
    .finally(process.exit)
}

module.exports = generateDevData
