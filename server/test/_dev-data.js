/* eslint-disable no-restricted-syntax, no-await-in-loop, import/no-extraneous-dependencies, security/detect-object-injection, camelcase, prefer-destructuring, no-param-reassign */
const { Client } = require('pg')
const fs = require('fs').promises
const yaml = require('js-yaml')
const get = require('lodash.get')
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
  const client = new Client({ connectionString: process.env.DATABASE_URL })
  await client.connect()
  return client
}

async function cleanDatabase(client) {
  await client.query(`truncate ${TABLES.reverse().join(', ')} cascade;`)
  return client
}

async function makeUsers(client) {
  // Ivy: anonymous
  // Jasmine: new/learner
  // Doris: established/contributor
  // Esther: admin
  function prep(result) {
    return get(result, 'rows[0]')
  }

  const ivy = prep(
    await client.query(`select * from sg_public.get_anonymous_token();`)
  )
  const jasmine = prep(
    await client.query(
      `select * from sg_public.sign_up('Jasmine', 'jasmine@example.com', 'example1');`
    )
  )
  const doris = prep(
    await client.query(
      `select * from sg_public.sign_up('Doris', 'doris@example.com', 'example1');`
    )
  )
  const esther = prep(
    await client.query(
      `select * from sg_public.sign_up('Esther', 'esther@example.com', 'example1');`
    )
  )
  return { ivy, jasmine, doris, esther }
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

async function makeSubjects(client, { users }) {
  await letsJwtIn(client, users.doris)

  const subjects = {}

  const emusYaml = yaml.safeLoad(
    await fs.readFile('./sample-subject.yaml', 'utf8')
  )
  for (const [key, { name, body, parent, before }] of Object.entries(
    emusYaml.subjects
  )) {
    subjects[key] = (await client.query(
      `
      select * from sg_public.new_subject(
        $1, -- language
        $2, -- name
        $3, -- tags
        $4, -- body
        $5, -- parent
        $6  -- before
      );`,
      [
        'en',
        name,
        [],
        body,
        parent ? [subjects[parent].entity_id] : [],
        before ? before.map(slug => subjects[slug].entity_id) : [],
      ]
    )).rows[0]
  }

  const sugYaml = yaml.safeLoad(
    await fs.readFile('./sample-subjects.yaml', 'utf8')
  )
  for (const { name, body } of sugYaml) {
    subjects[name] = (await client.query(
      `
      select sg_public.new_subject(
        $1, -- language
        $2, -- name
        $3, -- tags
        $4, -- body
        $5, -- parent
        $6  -- before
      );`,
      ['en', name, [], body, [], []]
    )).rows[0]
  }

  await client.query(
    `update sg_public.subject_version set status = 'accepted';`
  )

  return subjects
}

async function makeCards(client, { users, subjects }) {
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

  for (const { subject, video_id } of emusYaml.cards.video) {
    cards.video[subject] = (await client.query(
      `
        select * from sg_public.new_card(
          $1, -- language
          $2, -- name
          $3, -- tags
          $4, -- subject_id
          $5::sg_public.card_kind, -- kind
          $6  -- data
        )
      `,
      [
        'en',
        `Video: ${subjects[subject].name}`,
        [],
        subjects[subject].entity_id,
        'video',
        JSON.stringify({ video_id, site: 'youtube' }),
      ]
    )).rows[0]
  }

  for (const { subject, name, url } of emusYaml.cards.unscored_embed) {
    cards.unscoredEmbed[subject] = cards.unscoredEmbed[subject] || []
    cards.unscoredEmbed[subject].push(
      (await client.query(
        `
        select * from sg_public.new_card(
          $1, -- language
          $2, -- name
          $3, -- tags
          $4, -- subject_id
          $5::sg_public.card_kind, -- kind
          $6  -- data
        )
      `,
        [
          'en',
          name,
          [],
          subjects[subject].entity_id,
          'unscored_embed',
          JSON.stringify({ url }),
        ]
      )).rows[0]
    )
  }

  for (const { subject, name, body } of emusYaml.cards.page) {
    cards.page[subject] = (await client.query(
      `
        select * from sg_public.new_card(
          $1, -- language
          $2, -- name
          $3, -- tags
          $4, -- subject_id
          $5::sg_public.card_kind, -- kind
          $6  -- data
        )
      `,
      [
        'en',
        name,
        [],
        subjects[subject].entity_id,
        'page',
        JSON.stringify({ body }),
      ]
    )).rows[0]
  }

  for (const { subject, body, options } of emusYaml.cards.choice) {
    cards.choice[subject] = cards.choice[subject] || []
    cards.choice[subject].push(
      (await client.query(
        `
        select * from sg_public.new_card(
          $1, -- language
          $2, -- name
          $3, -- tags
          $4, -- subject_id
          $5::sg_public.card_kind, -- kind
          $6  -- data
        )
      `,
        [
          'en',
          body,
          [],
          subjects[subject].entity_id,
          'choice',
          JSON.stringify({
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
          }),
        ]
      )).rows[0]
    )
  }

  return cards
}

/*
async function makeUserSubjects(client, { users, subjects }) {
  const userSubjects = {}

  await letsJwtIn(client, users.doris)
  userSubjects.doris = (await client.query(`
    insert into sg_public.user_subject
    (subject_id) values ('${subjects.all.entity_id}')
  `)).rows[0]

  await letsJwtIn(client, users.esther)
  userSubjects.esther = (await client.query(`
    insert into sg_public.user_subject
    (subject_id) values ('${subjects.foundation.entity_id}')
  `)).rows[0]

  return {}
}

async function makeResponses(client, { users, cards }) {
  await letsJwtIn(client, users.doris)

  const responses = {}

  const subjectsToHit = ['intro', 'params', 'human', 'digital', 'complex']

  for (const subj of subjectsToHit) {
    const card = cards.choice[subj][0]
    responses[subj] = (await client.query(`
      insert into sg_public.response
      (card_id, response)
      values
      ('${card.entity_id}', '${
      Object.entries(card.data.options)
        .filter(([, opt]) => opt.correct)
        .map(([key]) => key)[0]
    }');
    `)).rows[0]
  }

  return responses
}
*/

async function generateDevData() {
  const users = {}
  const subjects = {}
  const cards = {}
  const userSubjects = {}
  const responses = {}
  const data = { users, subjects, cards, userSubjects, responses }

  if (process.env.NODE_ENV === 'production') {
    return data
  }

  const client = await makeClient()
  await cleanDatabase(client)
  Object.assign(users, await makeUsers(client, data))
  Object.assign(subjects, await makeSubjects(client, data))
  Object.assign(cards, await makeCards(client, data))
  // Object.assign(userSubjects, await makeUserSubjects(client, data))
  // Object.assign(responses, await makeResponses(client, data))
  await letsJwtOut(client)

  return data
}

if (require.main === module) {
  generateDevData()
    .catch(console.error) // eslint-disable-line
    .finally(process.exit)
}

module.exports = generateDevData
