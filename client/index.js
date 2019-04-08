/* eslint-disable max-params, no-console, max-lines */
const path = require('path')
const express = require('express')
const bodyParser = require('body-parser')
const cookieParser = require('cookie-parser')
const jwt = require('jsonwebtoken')
const get = require('lodash.get')
const {
  convertUuid58ToUuid: toU,
  convertUuidToUuid58: to58,
} = require('uuid58')
const GQL = require('./util/gql-queries')
const getGqlErrors = require('./util/gql-errors')

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

const cacheHash =
  process.env.NODE_ENV === 'test' ? '_' : Date.now().toString(36)

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

function handleError(err, req, res, next) {
  // See express-async-errors
  if (err) res.redirect('/server-error')
  next(err)
}

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

function handleRegular(req, res) {
  return res.render('Index', {
    location: req.url,
    query: req.query,
    cacheHash,
    role: getRole(req),
  })
}

function clientizeKind(s) {
  return s.toLowerCase().replace(/_/g, '-')
}

app.use(ensureJwt)
app.use(handleError)

// /////////////////////////////////////////////////////////////////////////////

app.get('/sitemap.txt', (req, res) =>
  res.send(`
https://sagefy.org
https://sagefy.org/terms
https://sagefy.org/contact
https://sagefy.org/sign-up
https://sagefy.org/log-in
https://sagefy.org/email
https://sagefy.org/password
`)
) // Add more public routes as they are available

app.get('/learn-:kind/:cardId', async (req, res) => {
  const gqlRes = await GQL.learnGetCard(req, {
    cardId: toU(req.params.cardId),
    subjectId: toU(req.cookies.step),
  })
  const card = get(gqlRes, 'data.cardByEntityId')
  if (!card || clientizeKind(card.kind) !== req.params.kind) {
    return res.redirect('/server-error')
  }
  return res.render('Index', {
    ...card,
    location: req.url,
    query: req.query,
    cacheHash,
    role: getRole(req),
    progress: get(gqlRes, 'data.selectSubjectLearned'),
  })
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
  return res.render('Index', {
    ...req.body,
    ...card,
    location: req.url,
    query: req.query,
    cacheHash,
    role: getRole(req),
    progress: get(gqlRes2, 'data.createResponse.response.learned'),
  })
})

app.get('/sign-up', isAnonymous, handleRegular)

app.post('/sign-up', isAnonymous, async (req, res) => {
  const gqlRes = await GQL.rootNewUser(req, req.body)
  const gqlErrors = getGqlErrors(gqlRes)
  if (Object.keys(gqlErrors).length) {
    return res.render('Index', {
      location: req.url,
      cacheHash,
      gqlErrors,
      prevValues: req.body,
      query: req.query,
    })
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
    return res.render('Index', {
      location: req.url,
      cacheHash,
      gqlErrors,
      prevValues: req.body,
      query: req.query,
    })
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

function getQueryState(req) {
  return parseInt(req.query.state, 10) || 0
}

app.get('/email', async (req, res) => {
  const state = getQueryState(req)
  return res.render('Index', { location: req.url, cacheHash, state })
})

app.post('/email', async (req, res) => {
  if (getQueryState(req) === 2) {
    const gqlRes = await GQL.rootEditEmail(
      {
        cookies: { [JWT_COOKIE_NAME]: req.query.token },
      },
      req.body
    )
    const gqlErrors = getGqlErrors(gqlRes)
    if (Object.keys(gqlErrors).length) {
      return res.render('Index', {
        location: req.url,
        cacheHash,
        gqlErrors,
        state: 2,
      })
    }
    return res.redirect('/log-in')
  }
  const gqlRes = await GQL.rootNewEmailToken(req, req.body)
  const gqlErrors = getGqlErrors(gqlRes)
  if (Object.keys(gqlErrors).length) {
    return res.render('Index', {
      location: req.url,
      cacheHash,
      gqlErrors,
      state: 0,
    })
  }
  return res.redirect('/email?state=1')
})

app.get('/password', async (req, res) => {
  const state = getQueryState(req)
  return res.render('Index', { location: req.url, cacheHash, state })
})

app.post('/password', async (req, res) => {
  if (getQueryState(req) === 2) {
    const gqlRes = await GQL.rootEditPassword(
      {
        cookies: { [JWT_COOKIE_NAME]: req.query.token },
      },
      req.body
    )
    const gqlErrors = getGqlErrors(gqlRes)
    if (Object.keys(gqlErrors).length) {
      return res.render('Index', {
        location: req.url,
        cacheHash,
        gqlErrors,
        state: 2,
      })
    }
    return res.redirect('/log-in')
  }
  const gqlRes = await GQL.rootNewPasswordToken(req, req.body)
  const gqlErrors = getGqlErrors(gqlRes)
  if (Object.keys(gqlErrors).length) {
    return res.render('Index', {
      location: req.url,
      cacheHash,
      gqlErrors,
      state: 0,
    })
  }
  return res.redirect('/password?state=1')
})

app.get('/settings', isUser, async (req, res) => {
  const gqlRes = await GQL.rootGetCurrentUser(req)
  return res.render('Index', {
    location: req.url,
    cacheHash,
    prevValues: get(gqlRes, 'data.getCurrentUser'),
  })
})

app.post('/settings', isUser, async (req, res) => {
  const gqlRes = await GQL.rootEditUser(req, req.body)
  const gqlErrors = getGqlErrors(gqlRes)
  return res.render('Index', {
    location: req.url,
    cacheHash,
    gqlErrors,
    prevValues: req.body,
  })
})

app.get('/log-out', isUser, (req, res) =>
  res.clearCookie(JWT_COOKIE_NAME).redirect('/')
)

app.get('/dashboard', isUser, async (req, res) => {
  const gqlRes = await GQL.learnListUsubj(req)
  return res.render('Index', {
    location: req.url,
    cacheHash,
    role: getRole(req),
    allUserSubjects: {
      nodes: get(gqlRes, 'data.allUserSubjects.nodes', []).map(
        ({ id, subject: { entityId, name, body } }) => ({
          id,
          entityId,
          name,
          body,
        })
      ),
    },
    name: get(gqlRes, 'data.getCurrentUser.name'),
  })
})

app.get('/search-subjects', async (req, res) => {
  const gqlRes = await GQL.learnSearchSubject(req, req.query)
  return res.render('Index', {
    location: req.url,
    query: req.query,
    cacheHash,
    role: getRole(req),
    searchSubjects: get(gqlRes, 'data.searchSubjects'),
  })
})

app.post('/create-subject', async (req, res) => {
  const gqlRes = await GQL.contributeNewSubject(req, req.body)
  const gqlErrors = getGqlErrors(gqlRes)
  if (Object.keys(gqlErrors).length) {
    return res.render('Index', {
      location: req.url,
      cacheHash,
      gqlErrors,
      prevValues: req.body,
    })
  }
  const role = getRole(req)
  const { entityId, name } = get(gqlRes, 'data.newSubject.subjectVersion', {})
  if (role === 'sg_anonymous') {
    return res.redirect(`/search-subjects?q=${name}`)
  }
  await GQL.learnNewUsubj(req, { subjectId: entityId })
  return res.redirect('/dashboard')
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
  return res.render('Index', {
    location: req.url,
    query: req.query,
    cacheHash,
    role,
    subjects,
  })
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

app.get('/', async (req, res) => {
  const gqlRes = await GQL.learnHome(req)
  return res.render('Index', {
    location: req.url,
    cacheHash,
    role: getRole(req),
    selectPopularSubjects: get(gqlRes, 'data.selectPopularSubjects'),
  })
})

// For pages that don't have specific data requirements
// and don't require being logged in or logged out:
// GET /create-card
// GET /create-subject
// GET /server-error
// GET /terms
// GET /contact
// GET /
// GET * (NotFound)
app.get('*', handleRegular)

// /////////////////////////////////////////////////////////////////////////////

if (require.main === module) {
  app.listen(process.env.PORT || 5984)
}

module.exports = app
