const express = require('express')
const morgan = require('morgan')

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

const app = express()
app.use(morgan('tiny'))

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

/* eslint-disable max-params */
app.use((err, req, res, next) => {
  if (err.message === 'access denied') {
    res.status(403)
    res.json({ error: err.message })
  }
  next(err)
})
/* eslint-enable */

/* eslint-disable no-console */
app.listen(8654, () => console.log('Listening on port 8654.'))
/* eslint-enable */

// https://gist.github.com/zerbfra/70b155fa00b4e0d6fd1d4e090a039ad4
