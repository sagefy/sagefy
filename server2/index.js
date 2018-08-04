const express = require('express')
const helmet = require('helmet')
const morgan = require('morgan')
const session = require('express-session')
const RedisStore = require('connect-redis')(session)

const config = require('./config')

const errorMiddleware = require('./middleware/errorMiddleware')

const indexRouter = require('./routes/index')
const sessionsRouter = require('./routes/sessions')
const usersRouter = require('./routes/users')
const userSubjectsRoute = require('./routes/userSubjects')
const noticesRouter = require('./routes/notices')
const followsRouter = require('./routes/follows')
const topicsRouter = require('./routes/topics')
const postsRouter = require('./routes/posts')
const unitsRouter = require('./routes/units')
const subjectsRouter = require('./routes/subjects')
const cardsRouter = require('./routes/cards')

require('express-async-errors')

const TWO_WEEKS_IN_MS = 1000 * 60 * 60 * 24 * 7 * 2

const app = express()
app.use(morgan('tiny'))
app.use(helmet())
app.use(errorMiddleware)
app.use(
  session({
    secret: config.session.secret,
    store: new RedisStore(config.redis),
    cookie: {
      maxAge: TWO_WEEKS_IN_MS,
    },
    resave: false,
    saveUninitialized: false,
  })
)

app.use('/x', indexRouter)
app.use('/x/sessions', sessionsRouter)
app.use('/x/users', usersRouter)
app.use('/x/users')
app.use('/x/users/:userId/subjects', userSubjectsRoute)
app.use('/x/notices', noticesRouter)
app.use('/x/follows', followsRouter)
app.use('/x/topics', topicsRouter)
app.use('/x/topics/:topicId/posts', postsRouter)
app.use('/x/units', unitsRouter)
app.use('/x/subjects', subjectsRouter)
app.use('/x/cards', cardsRouter)

/* eslint-disable no-console */
app.listen(8654, () => console.log('Listening on port 8654.'))
/* eslint-enable */

// https://gist.github.com/zerbfra/70b155fa00b4e0d6fd1d4e090a039ad4
