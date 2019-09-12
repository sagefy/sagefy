/* eslint-disable max-lines */
const path = require('path')
const express = require('express')
const bodyParser = require('body-parser')
const cookieParser = require('cookie-parser')
const jwt = require('jsonwebtoken')
const get = require('lodash.get')
const set = require('lodash.set')
const fromPairs = require('lodash.frompairs')
const { toU, to58 } = require('uuid58')
const uuidv4 = require('uuid/v4')
const request = require('request-promise-native')
const CARD_KIND = require('./util/card-kind')
const GQL = require('./util/gql-queries')
const getGqlErrors = require('./util/gql-errors')
const isUuid = require('./util/is-uuid')

const JWT_COOKIE_NAME = 'jwt'
const JWT_COOKIE_PARAMS = {
  maxAge: 1000 * 60 * 60 * 24, // 1 day in milliseconds
  httpOnly: true,
  secure: process.env.NODE_ENV === 'production',
}
const LEARN_COOKIE_PARAMS = {
  ...JWT_COOKIE_PARAMS,
  maxAge: 1000 * 60 * 60, // 1 hour in milliseconds
}

require('express-async-errors')

const hash = Date.now().toString(36)

const app = express()

app.use(bodyParser.urlencoded({ extended: false }))
app.use(cookieParser())

// See https://github.com/reactjs/express-react-views#add-it-to-your-app
app.set('views', path.join(__dirname, '/views'))
app.set('view engine', 'jsx')
app.engine('jsx', require('express-react-views').createEngine())

async function ensureJwt(req, res, next) {
  if (get(req.cookies, JWT_COOKIE_NAME)) return next()
  const gqlRes = await GQL.getAnonymousToken(req)
  const jwtToken = get(gqlRes, 'anonymousToken.jwtToken')
  res.cookie(JWT_COOKIE_NAME, jwtToken, JWT_COOKIE_PARAMS)
  return next()
}

/* eslint-disable max-params */
function handleError(err, req, res, next) {
  // See express-async-errors
  if (err) return res.status(500).render('ServerErrorPage')
  return next(err)
}
/* eslint-enable */

function getJwt(req) {
  const jwtCookie = get(req.cookies, JWT_COOKIE_NAME)
  if (!jwtCookie) return {}
  return jwt.decode(jwtCookie)
}

function getRole(req) {
  return get(getJwt(req), 'role')
}

function isUser(req, res, next) {
  if (!['sg_user', 'sg_admin'].includes(getRole(req))) {
    return res.redirect('/log-in')
  }
  return next()
}

function isAnonymous(req, res, next) {
  if (getRole(req) !== 'sg_anonymous') {
    return res.redirect('/dashboard')
  }
  return next()
}

function setResLocals(req, res, next) {
  res.locals.hash = hash
  res.locals.url = req.url
  res.locals.query = req.query
  res.locals.body = req.body
  res.locals.params = req.params
  res.locals.role = getRole(req)
  return next()
}

function convertBodyToVars(body) {
  const values = {}
  Object.keys(body)
    .map(key => [key, key.replace(/\$/g, '.')])
    .forEach(([key, xpath]) => set(values, xpath, get(body, key)))
  return values
}

app.use(ensureJwt)
app.use(handleError)
app.use(setResLocals)

// SUBJECTS ////////////////////////////////////////////////////////////////////

app.get('/subjects/search', async (req, res) => {
  if (!req.query.q) return res.render('SearchSubjectsPage')
  const gqlRes = await GQL.searchSubjects(req, req.query)
  const subjects = get(gqlRes, 'searchSubjects.nodes')
  return res.render('SearchSubjectsPage', { subjects })
})

app.get('/subjects/create', (req, res) => res.render('CreateSubjectPage'))

app.post('/subjects/create', async (req, res) => {
  let gqlRes
  try {
    gqlRes = await GQL.createSubject(req, req.body)
  } catch (e) {
    const gqlErrors = getGqlErrors(e)
    return res.render('CreateSubjectPage', { gqlErrors })
  }
  const { entityId } = get(gqlRes, 'createSubject.subjectVersion', {})
  return res.redirect(`/subjects/${to58(entityId)}`)
})

app.get('/((subjects|learn-about))/(*-)?:subjectId', async (req, res, next) => {
  const entityId = toU(req.params.subjectId)
  if (!isUuid(entityId)) return next()
  const gqlRes = await GQL.getSubjectPage(req, { entityId })
  const subject = get(gqlRes, 'subjectByEntityId')
  // -- photos for the twitter feed
  // TODO lets store these in the database and make them editable
  const response = await request({
    uri: `https://www.flickr.com/services/rest`,
    qs: {
      method: 'flickr.photos.search',
      api_key: process.env.FLICKR_API_KEY,
      text: subject.name,
      per_page: 1,
      format: 'json',
      nojsoncallback: 1,
    },
    json: true,
  })
  const { farm, server, id, secret } = get(response, 'photos.photo[0]', {})
  if (id && farm && server && secret) {
    subject.image = `https://farm${farm}.static.flickr.com/${server}/${id}_${secret}.jpg`
  }
  return res.render('SubjectPage', { subject })
})

app.get('/subjects/:subjectId/talk', async (req, res) => {
  const gqlRes = await GQL.listSubjectPosts(req, {
    entityId: toU(req.params.subjectId),
  })
  const entity = get(gqlRes, 'subjectByEntityId')
  const topics = get(gqlRes, 'allTopics.nodes')
  return res.render('TalkSubjectPage', { entity, topics })
})

app.get('/subjects/:subjectId/history', async (req, res) => {
  const gqlRes = await GQL.listSubjectVersions(req, {
    entityId: toU(req.params.subjectId),
  })
  const subject = get(gqlRes, 'subjectByEntityId')
  const versions = get(gqlRes, 'allSubjectVersions.nodes')
  return res.render('ViewHistorySubjectPage', { subject, versions })
})

app.get('/subjects/:subjectId/edit', async (req, res, next) => {
  const subjGqlRes = await GQL.getSubject(req, {
    entityId: toU(req.params.subjectId),
  })
  const subject = get(subjGqlRes, 'subjectByEntityId')
  if (!subject) next()
  return res.render('EditSubjectPage', { subject })
})

app.post('/subjects/:subjectId/edit', async (req, res, next) => {
  const subjGqlRes = await GQL.getSubject(req, {
    entityId: toU(req.params.subjectId),
  })
  const subject = get(subjGqlRes, 'subjectByEntityId')
  if (!subject) next()
  try {
    await GQL.updateSubject(req, {
      entityId: toU(req.body.entityId),
      name: req.body.name,
      body: req.body.body,
      before: get(subject, 'beforeSubjects.nodes', []).map(
        ({ entityId }) => entityId
      ), // temporary
      parent: get(subject, 'parentSubjects.nodes', []).map(
        ({ entityId }) => entityId
      ), // temporary
    })
    return res.redirect(`/subjects/${req.params.subjectId}`) // todo use return from updateSubject forid
  } catch (e) {
    const gqlErrors = getGqlErrors(e)
    return res.render('EditSubjectPage', { subject, gqlErrors })
  }
})

app.get('/subjects/:subjectId/steps', async (req, res) => {
  const gqlRes = await GQL.chooseSubject(req, {
    subjectId: toU(req.params.subjectId),
  })
  const subject = get(gqlRes, 'subjectByEntityId')
  const subjects = get(gqlRes, 'subjectByEntityId.nextChildSubjects.nodes')
  return res.render('ChooseStepPage', { subject, subjects })
})

app.get('/subjects/:subjectId/complete', async (req, res, next) => {
  const subjGqlRes = await GQL.getSubject(req, {
    entityId: toU(req.params.subjectId),
  })
  const subject = get(subjGqlRes, 'subjectByEntityId')
  if (!subject) next()
  return res.render('CompleteSubjectPage', { subject })
})

// CARDS ///////////////////////////////////////////////////////////////////////

function transformValuesForChoice(values) {
  /* eslint-disable camelcase */
  const { name } = values
  const { max_options_to_show, options, correct } = values.data
  const data = {
    body: name,
    max_options_to_show: parseInt(max_options_to_show, 10),
    options: fromPairs(
      Object.keys(options).map(i => [
        isUuid(i) ? i : uuidv4(),
        { ...get(options, i), correct: correct === i.toString() },
      ])
    ),
  }
  return { ...values, data }
  /* eslint-enable */
}

app.get('/(:kind-)?cards/create', async (req, res, next) => {
  if (!req.query.subjectId) res.redirect('/')
  const subjGqlRes = await GQL.getSubject(req, {
    entityId: toU(req.query.subjectId),
  })
  const subject = get(subjGqlRes, 'subjectByEntityId')
  if (!subject) return next()
  return res.render(
    `Create${get(CARD_KIND, [req.params.kind, 'page'], '')}CardPage`,
    { subject }
  )
})

app.post('/(:kind-)?cards/create', async (req, res) => {
  let values = convertBodyToVars(req.body)
  values.subjectId = toU(values.subjectId)
  if (req.body.kind === 'CHOICE') {
    values = transformValuesForChoice(values)
  }
  try {
    await GQL.createCard(req, values)
    // TODO redirect based on how we got here
    return res.redirect(`/next?step=${req.cookies.step}`)
  } catch (e) {
    const gqlErrors = getGqlErrors(e)
    return res.render(
      `Create${get(CARD_KIND, [req.params.kind, 'page'], '')}CardPage`,
      { gqlErrors }
    )
  }
})

app.get('/(:kind-)?cards/:cardId', async (req, res) => {
  const gqlRes = await GQL.getCard(req, {
    cardId: toU(req.params.cardId),
  })
  const card = get(gqlRes, 'cardByEntityId')
  return res.render(`${get(CARD_KIND, [card.kind, 'page'], '')}CardPage`, {
    card,
  })
})

app.get('/(:kind-)?cards/:cardId/history', async (req, res) => {
  const gqlRes = await GQL.listCardVersions(req, {
    entityId: toU(req.params.cardId),
  })
  const card = get(gqlRes, 'cardByEntityId')
  const versions = get(gqlRes, 'allCardVersions.nodes')
  return res.render(
    `ViewHistory${get(CARD_KIND, [card.kind, 'page'], '')}CardPage`,
    { card, versions }
  )
})

app.get('/(:kind-)?cards/:cardId/talk', async (req, res) => {
  const gqlRes = await GQL.listCardPosts(req, {
    entityId: toU(req.params.cardId),
  })
  const entity = get(gqlRes, 'cardByEntityId')
  const topics = get(gqlRes, 'allTopics.nodes')
  return res.render(`Talk${get(CARD_KIND, [entity.kind, 'page'])}CardPage`, {
    entity,
    topics,
  })
})

app.get('/(:kind-)?cards/:cardId/edit', async (req, res) => {
  const gqlRes = await GQL.getCard(req, {
    cardId: toU(req.params.cardId),
  })
  const card = get(gqlRes, 'cardByEntityId')
  const subject = get(card, 'subject')
  return res.render(`Edit${get(CARD_KIND, [card.kind, 'page'], '')}CardPage`, {
    card,
    subject,
  })
})

app.post('/(:kind-)?cards/:cardId/edit', async (req, res) => {
  const cardId = toU(req.params.cardId)
  let values = convertBodyToVars(req.body)
  values.subjectId = toU(values.subjectId)
  values.entityId = cardId
  if (req.body.kind === 'CHOICE') {
    values = transformValuesForChoice(values)
  }
  try {
    const gqlRes = await GQL.updateCard(req, values)
    const card = get(gqlRes, 'updateCard.cardVersion')
    const redirectUrl = req.query.redirect
      ? decodeURIComponent(req.query.redirect)
      : `/${get(CARD_KIND, [card.kind, 'url'])}-cards/${to58(card.entityId)}`
    return res.redirect(redirectUrl)
  } catch (e) {
    const gqlErrors = getGqlErrors(e)
    const gqlRes = await GQL.getCard(req, { cardId })
    const card = get(gqlRes, 'cardByEntityId')
    const subject = get(card, 'subject')
    return res.render(
      `Edit${get(CARD_KIND, [card.kind, 'page'], '')}CardPage`,
      {
        gqlErrors,
        card,
        subject,
        body: { ...req.body, options: values.options },
      }
    )
  }
})

app.get('/(:kind-)?cards/:cardId/learn', async (req, res, next) => {
  if (!req.cookies.step) {
    return res.redirect('/next')
  }
  const gqlRes = await GQL.getCardLearn(req, {
    cardId: toU(req.params.cardId),
    subjectId: toU(req.cookies.step),
  })
  const card = get(gqlRes, 'cardByEntityId')
  if (!card) return next()
  const subject = get(gqlRes, 'subjectByEntityId')
  const learned = get(gqlRes, 'subjectByEntityId.learned')
  return res.render(`Learn${get(CARD_KIND, [card.kind, 'page'])}CardPage`, {
    card,
    subject,
    learned,
  })
})

app.post('/((choice-))?cards/:cardId/learn', async (req, res, next) => {
  if (!req.body.choice) {
    return res.redirect(`/choice-cards/${req.params.cardId}/learn`)
  }
  const gqlRes = await GQL.getCardLearn(req, {
    cardId: toU(req.params.cardId),
    subjectId: toU(req.cookies.step),
  })
  const card = get(gqlRes, 'cardByEntityId')
  if (!card || card.kind !== 'CHOICE') {
    return next()
  }
  const gqlRes2 = await GQL.createResponse(req, {
    cardId: card.entityId,
    response: req.body.choice,
  })
  const learned = get(gqlRes2, 'createResponse.response.learned')
  const subject = get(gqlRes, 'subjectByEntityId')
  return res.render('LearnChoiceCardPage', { card, subject, learned })
})

app.post(
  ['/subjects/:subjectId/talk', '/(:kind-)?cards/:cardId/talk'],
  async (req, res) => {
    try {
      const gqlRes = await GQL.createTopic(req, req.body)
      const topicId = to58(get(gqlRes, 'createTopic.topic.id'))
      return res.redirect(`?topic-id=${topicId}#topic-${topicId}`)
    } catch (e) {
      return res.redirect('')
    }
  }
)

app.post(
  [
    '/subjects/:subjectId/talk/:topicId/post',
    '/(:kind-)?cards/:cardId/talk/:topicId/post',
  ],
  async (req, res) => {
    try {
      const gqlRes = await GQL.createPost(req, req.body)
      return res.redirect(
        `..?topic-id=${req.params.topicId}#post-${to58(
          get(gqlRes, 'createPost.post.id')
        )}`
      )
    } catch (e) {
      return res.redirect(`..?topic-id=${req.params.topicId}`)
    }
  }
)

// LOGGED-IN ///////////////////////////////////////////////////////////////////

app.get('/settings', isUser, async (req, res) => {
  const gqlRes = await GQL.getCurrentUser(req)
  const body = get(gqlRes, 'currentUser')
  return res.render('SettingsPage', { body })
})

app.post('/settings', isUser, async (req, res) => {
  try {
    await GQL.updateUser(req, req.body)
    return res.redirect('/settings')
  } catch (e) {
    const gqlErrors = getGqlErrors(e)
    return res.render('SettingsPage', { gqlErrors })
  }
})

app.get('/dashboard', isUser, async (req, res) => {
  const gqlRes = await GQL.listUserSubjects(req)
  const subjects = get(gqlRes, 'allUserSubjects.nodes', []).map(
    ({ id, subject: { entityId, name, body } }) => ({
      id,
      entityId,
      name,
      body,
    })
  )
  const mySubjects = get(gqlRes, 'subjectsByCurrentUser.nodes')
  const myCards = get(gqlRes, 'cardsByCurrentUser.nodes')
  const name = get(gqlRes, 'currentUser.name')
  return res.render('DashboardPage', { name, subjects, mySubjects, myCards })
})

// LOGGED-OUT //////////////////////////////////////////////////////////////////

app.get('/search', async (req, res) => {
  if (!req.query.q) return res.render('SearchPage')
  const gqlRes = await GQL.searchEntities(req, req.query)
  const results = get(gqlRes, 'searchEntities.nodes')
  return res.render('SearchPage', { results })
})

app.get('/next', async (req, res) => {
  const role = getRole(req)
  const defaultUrl = role === 'sg_anonymous' ? '/subjects/search' : '/dashboard'
  if (!req.query.goal && !req.cookies.goal) {
    return res.redirect(defaultUrl)
  }
  // ?goal => query.goal, undefined
  // ?step => cookie.goal, query.step
  // ?____ => cookie.goal, cookie.step
  const gqlRes = await GQL.next(req, {
    goal: toU(req.query.goal || req.cookies.goal),
    step: req.query.goal ? undefined : toU(req.query.step || req.cookies.step),
  })
  const { next, step, goal, kind, card } = get(gqlRes, 'next.nextPage')
  res.cookie('goal', to58(goal), LEARN_COOKIE_PARAMS)
  if (step) res.cookie('step', to58(step), LEARN_COOKIE_PARAMS)
  else res.clearCookie('step')
  const kindUrl = get(CARD_KIND, [kind, 'url'])
  const urlMap = {
    CREATE_CARD: `/cards/create?subjectId=${to58(step)}`,
    LEARN_CARD: `/${kindUrl}-cards/${to58(card)}/learn`,
    COMPLETE_SUBJECT: `/subjects/${to58(goal)}/complete`,
    CHOOSE_STEP: `/subjects/${to58(goal)}/steps`,
  }
  return res.redirect(get(urlMap, next, defaultUrl))
})

app.get('/users/:userId', async (req, res, next) => {
  const userId = toU(req.params.userId)
  if (!isUuid(userId)) return next()
  const gqlRes = await GQL.getUser(req, { userId })
  const user = get(gqlRes, 'userById')
  return res.render('UserPage', { user })
})

app.get('/sign-up', isAnonymous, (req, res) => res.render('SignUpPage'))

app.post('/sign-up', isAnonymous, async (req, res) => {
  try {
    const gqlRes = await GQL.createUser(req, req.body)
    const jwtToken = get(gqlRes, 'createUser.jwtToken')
    const redirectUrl =
      (req.query.redirect && decodeURIComponent(req.query.redirect)) ||
      '/dashboard'
    return res
      .cookie(JWT_COOKIE_NAME, jwtToken, JWT_COOKIE_PARAMS)
      .redirect(redirectUrl)
  } catch (e) {
    const gqlErrors = getGqlErrors(e)
    return res.render('SignUpPage', { gqlErrors })
  }
})

app.get('/log-in', isAnonymous, (req, res) => res.render('LogInPage'))

app.post('/log-in', isAnonymous, async (req, res) => {
  try {
    const gqlRes = await GQL.logIn(req, req.body)
    const jwtToken = get(gqlRes, 'logIn.jwtToken')
    const redirectUrl =
      (req.query.redirect && decodeURIComponent(req.query.redirect)) ||
      '/dashboard'
    return res
      .cookie(JWT_COOKIE_NAME, jwtToken, JWT_COOKIE_PARAMS)
      .redirect(redirectUrl)
  } catch (e) {
    const gqlErrors = getGqlErrors(e)
    return res.render('LogInPage', { gqlErrors })
  }
})

app.get('/log-out', isUser, (req, res) =>
  res.clearCookie(JWT_COOKIE_NAME).redirect('/')
)

app.get('/email', async (req, res) => res.render('AskEmailPage'))

app.post('/email', async (req, res) => {
  try {
    await GQL.createEmailToken(req, req.body)
    return res.redirect('/email/check')
  } catch (e) {
    const gqlErrors = getGqlErrors(e)
    return res.render('EmailAskPage', { gqlErrors })
  }
})

app.get('/email/check', async (req, res) => res.render('CheckEmailPage'))

app.get('/email/edit', async (req, res) => res.render('EditEmailPage'))

app.post('/email/edit', async (req, res) => {
  try {
    const cookies = { [JWT_COOKIE_NAME]: req.query.token }
    await GQL.updateEmail({ cookies }, req.body)
    return res.redirect('/log-in')
  } catch (e) {
    const gqlErrors = getGqlErrors(e)
    return res.render('EditEmailPage', { gqlErrors })
  }
})

app.get('/password', async (req, res) => res.render('AskPasswordPage'))

app.post('/password', async (req, res) => {
  try {
    await GQL.createPasswordToken(req, req.body)
    return res.redirect('/password/check')
  } catch (e) {
    const gqlErrors = getGqlErrors(e)
    return res.render('AskPasswordPage', { gqlErrors })
  }
})

app.get('/password/check', async (req, res) => res.render('CheckPasswordPage'))

app.get('/password/edit', async (req, res) => res.render('EditPasswordPage'))

app.post('/password/edit', async (req, res) => {
  try {
    const cookies = { [JWT_COOKIE_NAME]: req.query.token }
    await GQL.updatePassword({ cookies }, req.body)
    return res.redirect('/log-in')
  } catch (e) {
    const gqlErrors = getGqlErrors(e)
    return res.render('EditPasswordPage', { gqlErrors })
  }
})

app.get('/statistics', async (req, res) => {
  const statistics = await GQL.listStatistics(req)
  return res.render('StatisticsPage', { statistics })
})

app.get('/terms', (req, res) => res.render('TermsPage'))

app.get('/contact', (req, res) => res.render('ContactPage'))

app.get('/about', (req, res) => res.render('AboutPage'))

app.get('/', async (req, res) => {
  const gqlRes = await GQL.getHome(req)
  const subjects = get(gqlRes, 'popularSubjects.nodes')
  const whatIs = get(gqlRes, 'whatIsSagefy')
  if (whatIs) subjects.unshift(whatIs)
  return res.render('HomePage', { subjects })
})

const ROOT_PAGES = [
  '', // home
  '/terms',
  '/contact',
  '/about',
  '/sign-up',
  '/log-in',
  '/email',
  '/password',
  '/search',
  '/subjects/search',
  '/subjects/create',
  '/statistics',
]

app.get('/sitemap.txt', async (req, res) => {
  const gqlRes = await GQL.getSitemap(req)
  const subjects = get(gqlRes, 'allSubjects.nodes', []).map(
    ({ entityId, slug }) => `/learn-about/${slug}-${to58(entityId)}`
  )
  const cards = get(gqlRes, 'allCards.nodes', []).map(
    ({ entityId, kind }) =>
      `/${get(CARD_KIND, [kind, 'url'])}-cards/${to58(entityId)}`
  )
  const users = get(gqlRes, 'allUsers.nodes', []).map(
    ({ id }) => `/users/${to58(id)}`
  )
  const root =
    process.env.NODE_ENV === 'production' ? 'https://sagefy.org' : 'localhost'
  res.set('Content-Type', 'text/plain').send(
    ROOT_PAGES.concat(subjects)
      .concat(cards)
      .concat(users)
      .map(u => `${root}${u}`)
      .join('\n')
  )
}) // Add more public routes as they are available

app.get('*', (req, res) => res.status(404).render('NotFoundPage'))

// /////////////////////////////////////////////////////////////////////////////

/* eslint-disable no-console */
if (require.main === module) {
  console.log('Client running on port', process.env.CLIENT_PORT)
  app.listen(process.env.CLIENT_PORT)
}
/* eslint-enable */

module.exports = app
