/* eslint-disable max-lines */
const path = require('path')
const express = require('express')
const bodyParser = require('body-parser')
const cookieParser = require('cookie-parser')
const jwt = require('jsonwebtoken')
const get = require('lodash.get')
const set = require('lodash.set')
const fromPairs = require('lodash.frompairs')
const {
  convertUuid58ToUuid: toU,
  convertUuidToUuid58: to58,
} = require('uuid58')
const uuidv4 = require('uuid/v4')
const request = require('request-promise-native')
const GQL = require('./util/gql-queries')
const getGqlErrors = require('./util/gql-errors')

const hash = Date.now().toString(36)

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

const app = express()

app.use(bodyParser.urlencoded({ extended: false }))
app.use(cookieParser())

// See https://github.com/reactjs/express-react-views#add-it-to-your-app
app.set('views', path.join(__dirname, '/views'))
app.set('view engine', 'jsx')
app.engine('jsx', require('express-react-views').createEngine())

async function ensureJwt(req, res, next) {
  if (!get(req.cookies, JWT_COOKIE_NAME)) {
    res.cookie(
      JWT_COOKIE_NAME,
      get(await GQL.rootGetAnonToken(req), 'data.getAnonymousToken.jwtToken'),
      JWT_COOKIE_PARAMS
    )
  }
  next()
}

/* eslint-disable max-params */
function handleError(err, req, res, next) {
  // See express-async-errors
  if (err) res.redirect('/server-error')
  next(err)
}
/* eslint-enable */

function getJwt(req) {
  return jwt.decode(get(req.cookies, JWT_COOKIE_NAME))
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

function formatData(req) {
  return {
    hash,
    url: req.url,
    query: req.query,
    body: req.body,
    params: req.params,
    role: getRole(req),
  }
}

function handleRegular(req, res) {
  return res.render('Index', formatData(req))
}

function clientizeKind(s) {
  return s.toLowerCase().replace(/_/g, '-')
}

function getQueryState(req) {
  return parseInt(req.query.state, 10) || 0
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

// /////////////////////////////////////////////////////////////////////////////

const ROOT_PAGES = [
  '', // home
  '/terms',
  '/contact',
  '/sign-up',
  '/log-in',
  '/email',
  '/password',
  '/search-subjects',
  '/create-subject',
  '/create-card',
  '/create-video-card',
  '/create-choice-card',
  '/create-page-card',
  '/create-unscored-embed-card',
]

const CARD_KIND_URL = {
  CHOICE: 'choice',
  VIDEO: 'video',
  PAGE: 'page',
  UNSCORED_EMBED: 'unscored-embed',
}

app.get('/sitemap.txt', async (req, res) => {
  const gqlRes = await GQL.dataSitemap(req)
  const subjects = get(gqlRes, 'data.allSubjects.nodes', []).map(
    ({ entityId }) => `/subjects/${to58(entityId)}`
  )
  const subjectTalk = get(gqlRes, 'data.allSubjects.nodes', []).map(
    ({ entityId }) => `/subjects/${to58(entityId)}/talk`
  )
  const cards = get(gqlRes, 'data.allCards.nodes', []).map(
    ({ entityId, kind }) =>
      `/${get(CARD_KIND_URL, kind)}-cards/${to58(entityId)}`
  )
  const cardTalk = get(gqlRes, 'data.allCards.nodes', []).map(
    ({ entityId, kind }) =>
      `/${get(CARD_KIND_URL, kind)}-cards/${to58(entityId)}/talk`
  )
  const users = get(gqlRes, 'data.allUsers.nodes', []).map(
    ({ id }) => `/users/${to58(id)}`
  )
  const root =
    process.env.NODE_ENV === 'production' ? 'https://sagefy.org' : 'localhost'
  res.set('Content-Type', 'text/plain').send(
    ROOT_PAGES.concat(subjects)
      .concat(subjectTalk)
      .concat(cards)
      .concat(cardTalk)
      .concat(users)
      .map(u => `${root}${u}`)
      .join('\n')
  )
}) // Add more public routes as they are available

app.get('/learn-:kind/:cardId', async (req, res) => {
  const gqlRes = await GQL.learnGetCard(req, {
    cardId: toU(req.params.cardId),
    subjectId: toU(req.cookies.step),
  })
  const card = get(gqlRes, 'data.cardByEntityId')
  if (!card || clientizeKind(card.kind) !== req.params.kind) {
    return res.redirect('/server-error')
  }
  const progress = get(gqlRes, 'data.selectSubjectLearned')
  return res.render('Index', { ...formatData(req), card, progress })
})

app.post('/learn-choice/:cardId', async (req, res) => {
  const gqlRes = await GQL.learnGetCard(req, {
    cardId: toU(req.params.cardId),
    subjectId: toU(req.cookies.step),
  })
  const card = get(gqlRes, 'data.cardByEntityId')
  if (!card || clientizeKind(card.kind) !== 'choice') {
    return res.redirect('/server-error')
  }
  const gqlRes2 = await GQL.learnRespondCard(req, {
    cardId: toU(req.params.cardId),
    response: req.body.choice,
  })
  const progress = get(gqlRes2, 'data.createResponse.response.learned')
  return res.render('Index', { ...formatData(req), card, progress })
})

app.get('/sign-up', isAnonymous, handleRegular)

app.post('/sign-up', isAnonymous, async (req, res) => {
  const gqlRes = await GQL.rootNewUser(req, req.body)
  const gqlErrors = getGqlErrors(gqlRes)
  if (Object.keys(gqlErrors).length) {
    return res.render('Index', { ...formatData(req), gqlErrors })
  }
  return res
    .cookie(
      JWT_COOKIE_NAME,
      get(gqlRes, 'data.signUp.jwtToken'),
      JWT_COOKIE_PARAMS
    )
    .redirect(
      (req.query.redirect && decodeURIComponent(req.query.redirect)) ||
        '/dashboard'
    )
})

app.get('/log-in', isAnonymous, handleRegular)

app.post('/log-in', isAnonymous, async (req, res) => {
  const gqlRes = await GQL.rootLogInUser(req, req.body)
  const gqlErrors = getGqlErrors(gqlRes)
  if (Object.keys(gqlErrors).length) {
    return res.render('Index', { ...formatData(req), gqlErrors })
  }
  return res
    .cookie(
      JWT_COOKIE_NAME,
      get(gqlRes, 'data.logIn.jwtToken'),
      JWT_COOKIE_PARAMS
    )
    .redirect(
      (req.query.redirect && decodeURIComponent(req.query.redirect)) ||
        '/dashboard'
    )
})

app.get('/email', async (req, res) => {
  const state = getQueryState(req)
  return res.render('Index', { ...formatData(req), state })
})

app.post('/email', async (req, res) => {
  // TODO split into two routes & pages
  if (getQueryState(req) === 2) {
    const gqlRes = await GQL.rootEditEmail(
      {
        cookies: { [JWT_COOKIE_NAME]: req.query.token },
      },
      req.body
    )
    const gqlErrors = getGqlErrors(gqlRes)
    if (Object.keys(gqlErrors).length) {
      return res.render('Index', { ...formatData(req), gqlErrors, state: 2 })
    }
    return res.redirect('/log-in')
  }
  const gqlRes = await GQL.rootNewEmailToken(req, req.body)
  const gqlErrors = getGqlErrors(gqlRes)
  if (Object.keys(gqlErrors).length) {
    return res.render('Index', { ...formatData(req), gqlErrors, state: 0 })
  }
  return res.redirect('/email?state=1')
})

app.get('/password', async (req, res) => {
  const state = getQueryState(req)
  return res.render('Index', { ...formatData(req), state })
})

app.post('/password', async (req, res) => {
  // TODO split into to routes & pages
  if (getQueryState(req) === 2) {
    const gqlRes = await GQL.rootEditPassword(
      {
        cookies: { [JWT_COOKIE_NAME]: req.query.token },
      },
      req.body
    )
    const gqlErrors = getGqlErrors(gqlRes)
    if (Object.keys(gqlErrors).length) {
      return res.render('Index', { ...formatData(req), gqlErrors, state: 2 })
    }
    return res.redirect('/log-in')
  }
  const gqlRes = await GQL.rootNewPasswordToken(req, req.body)
  const gqlErrors = getGqlErrors(gqlRes)
  if (Object.keys(gqlErrors).length) {
    return res.render('Index', { ...formatData(req), gqlErrors, state: 0 })
  }
  return res.redirect('/password?state=1')
})

app.get('/settings', isUser, async (req, res) => {
  const gqlRes = await GQL.rootGetCurrentUser(req)
  const body = get(gqlRes, 'data.getCurrentUser')
  return res.render('Index', { ...formatData(req), body })
})

app.post('/settings', isUser, async (req, res) => {
  const gqlRes = await GQL.rootEditUser(req, req.body)
  const gqlErrors = getGqlErrors(gqlRes)
  return res.render('Index', { ...formatData(req), gqlErrors })
})

app.get('/log-out', isUser, (req, res) =>
  res.clearCookie(JWT_COOKIE_NAME).redirect('/')
)

app.get('/dashboard', isUser, async (req, res) => {
  const gqlRes = await GQL.learnListUsubj(req)
  const subjects = get(gqlRes, 'data.allUserSubjects.nodes', []).map(
    ({ id, subject: { entityId, name, body } }) => ({
      id,
      entityId,
      name,
      body,
    })
  )
  const name = get(gqlRes, 'data.getCurrentUser.name')
  return res.render('Index', { ...formatData(req), subjects, name })
})

app.get('/search-subjects', async (req, res) => {
  const gqlRes = await GQL.learnSearchSubject(req, req.query)
  const subjects = get(gqlRes, 'data.searchSubjects.nodes')
  return res.render('Index', { ...formatData(req), subjects })
})

app.post('/create-subject', async (req, res) => {
  const gqlRes = await GQL.contributeNewSubject(req, req.body)
  const gqlErrors = getGqlErrors(gqlRes)
  if (Object.keys(gqlErrors).length) {
    return res.render('Index', { ...formatData(req), gqlErrors })
  }
  const role = getRole(req)
  const { entityId, name } = get(gqlRes, 'data.newSubject.subjectVersion', {})
  if (role === 'sg_anonymous') {
    return res.redirect(`/search-subjects?q=${name}`)
  }
  await GQL.learnNewUsubj(req, { subjectId: entityId })
  return res.redirect('/dashboard')
})

app.get('/create(-:kind)?-card', async (req, res) => {
  if (!req.query.subjectId) res.redirect('/')
  const subjGqlRes = await GQL.contributeGetSubject(req, {
    entityId: toU(req.query.subjectId),
  })
  const subject = get(subjGqlRes, 'data.subjectByEntityId')
  if (!subject) res.redirect('/server-error')
  return res.render('Index', { ...formatData(req), subject })
})

app.post('/create(-:kind)?-card', async (req, res) => {
  const values = convertBodyToVars(req.body)
  values.subjectId = toU(values.subjectId)
  if (req.body.kind === 'CHOICE') {
    values.data.body = values.name
    values.data.max_options_to_show = parseInt(
      values.data.max_options_to_show,
      10
    )
    values.data.options = fromPairs(
      [0, 1, 2, 3].map(i => [
        uuidv4(),
        {
          ...get(values.data.options, i),
          correct: values.data.correct === i.toString(),
        },
      ])
    )
    delete values.data.correct
  }
  const gqlRes = await GQL.contributeNewCard(req, values)
  const gqlErrors = getGqlErrors(gqlRes)
  if (Object.keys(gqlErrors).length) {
    return res.render('Index', { ...formatData(req), gqlErrors })
  }
  // TODO redirect based on how we got to create-card
  return res.redirect(`/next?step=${req.cookies.step}`)
})

app.get('/choose-step', async (req, res) => {
  const role = getRole(req)
  const { goal } = req.cookies
  if (!goal)
    return res.redirect(
      role === 'sg_anonymous' ? '/search-subjects' : '/dashboard'
    )
  const subjects = get(
    await GQL.learnChooseSubject(req, { subjectId: toU(goal) }),
    'data.selectSubjectToLearn.nodes'
  )
  if (!subjects || !subjects.length) {
    return res.redirect(
      role === 'sg_anonymous' ? '/search-subjects' : '/dashboard'
    )
  }
  if (subjects.length === 1) {
    return res.redirect(`/next?step=${to58(subjects[0].entityId)}`)
  }
  return res.render('Index', { ...formatData(req), subjects })
})

/* eslint-disable max-statements */
app.get('/next', async (req, res) => {
  let { goal, step } = req.cookies
  if (req.query.goal) {
    ;({ goal } = req.query)
    res.cookie('goal', goal, LEARN_COOKIE_PARAMS).clearCookie('step')
    step = null
    await GQL.learnNewUsubj(req, { subjectId: toU(goal) })
  }
  if (req.query.step) {
    ;({ step } = req.query)
    res.cookie('step', step, LEARN_COOKIE_PARAMS)
  }
  if (step) {
    const gqlRes = await GQL.learnGetLearned(req, { subjectId: toU(step) })
    if (get(gqlRes, 'data.selectSubjectLearned') >= 0.99) {
      return res.clearCookie('step').redirect('/choose-step')
    }
    const gqlRes2 = await GQL.learnChooseCard(req, { subjectId: toU(step) })
    const card = get(gqlRes2, 'data.selectCardToLearn.card')
    if (!card) return res.redirect(`/create-card?subjectId=${step}`)
    const { kind, entityId } = card
    return res.redirect(`/learn-${clientizeKind(kind)}/${to58(entityId)}`)
  }
  if (goal) return res.redirect('/choose-step')
  return res.redirect(
    getRole(req) === 'sg_anonymous' ? '/search-subjects' : '/dashboard'
  )
}) /* eslint-enable */

app.get('/subjects/:subjectId', async (req, res) => {
  const gqlRes = await GQL.dataGetSubject(req, {
    entityId: toU(req.params.subjectId),
  })
  const subject = get(gqlRes, 'data.subjectByEntityId')
  // -- photos for the twitter feed
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
  if (id) {
    subject.image = `https://farm${farm}.static.flickr.com/${server}/${id}_${secret}.jpg`
  }
  return res.render('Index', { ...formatData(req), subject })
})

app.get('/(:kind-)?cards/:cardId', async (req, res) => {
  const gqlRes = await GQL.dataGetCard(req, {
    cardId: toU(req.params.cardId),
  })
  const card = get(gqlRes, 'data.cardByEntityId')
  return res.render('Index', { ...formatData(req), card })
})

app.get('/users/:userId', async (req, res) => {
  const gqlRes = await GQL.dataGetUser(req, {
    userId: toU(req.params.userId),
  })
  const user = get(gqlRes, 'data.userById')
  return res.render('Index', { ...formatData(req), user })
})

app.get('/subjects/:subjectId/talk', async (req, res) => {
  const gqlRes = await GQL.contributeListPostsSubject(req, {
    entityId: toU(req.params.subjectId),
  })
  const entity = get(gqlRes, 'data.subjectByEntityId')
  const topics = get(gqlRes, 'data.allTopics.nodes')
  return res.render('Index', { ...formatData(req), entity, topics })
})

app.get('/(:kind-)?cards/:cardId/talk', async (req, res) => {
  const gqlRes = await GQL.contributeListPostsCard(req, {
    entityId: toU(req.params.cardId),
  })
  const entity = get(gqlRes, 'data.cardByEntityId')
  const topics = get(gqlRes, 'data.allTopics.nodes')
  return res.render('Index', { ...formatData(req), entity, topics })
})

app.post(
  ['/subjects/:subjectId/talk', '/(:kind-)?cards/:cardId/talk'],
  async (req, res) => {
    const gqlRes = await GQL.contributeNewTopic(req, req.body)
    const gqlErrors = getGqlErrors(gqlRes)
    if (Object.keys(gqlErrors).length) {
      return res.redirect('')
    }
    const topicId = to58(get(gqlRes, 'data.createTopic.topic.id'))
    return res.redirect(`?topic-id=${topicId}#topic-${topicId}`)
  }
)

app.post(
  [
    '/subjects/:subjectId/talk/:topicId/post',
    '/(:kind-)?cards/:cardId/talk/:topicId/post',
  ],
  async (req, res) => {
    const gqlRes = await GQL.contributeNewPost(req, req.body)
    const gqlErrors = getGqlErrors(gqlRes)
    if (Object.keys(gqlErrors).length) {
      return res.redirect(`..?topic-id=${req.params.topicId}`)
    }
    return res.redirect(
      `..?topic-id=${req.params.topicId}#post-${to58(
        get(gqlRes, 'data.createPost.post.id')
      )}`
    )
  }
)

app.get('/', async (req, res) => {
  const gqlRes = await GQL.learnHome(req)
  const subjects = get(gqlRes, 'data.selectPopularSubjects.nodes')
  const whatIs = get(gqlRes, 'data.whatIsSagefy')
  if (whatIs) subjects.unshift(whatIs)
  return res.render('Index', { ...formatData(req), subjects })
})

// For pages that don't have specific data requirements
// and don't require being logged in or logged out:
// GET /create-subject
// GET /server-error
// GET /terms
// GET /contact
// GET * (NotFound)
app.get('*', handleRegular)

// /////////////////////////////////////////////////////////////////////////////

/* eslint-disable no-console */
if (require.main === module) {
  console.log('Client running on port', process.env.CLIENT_PORT)
  app.listen(process.env.CLIENT_PORT)
}
/* eslint-enable */

module.exports = app
