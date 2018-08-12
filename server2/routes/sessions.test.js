const request = require('supertest')
const express = require('express')
const bodyParser = require('body-parser')

require('express-async-errors')

const sessionsRouter = require('./sessions')
const sessionMiddleware = require('../middleware/sessionMiddleware')
const errorMiddleware = require('../middleware/errorMiddleware')

describe('Sessions Routes', () => {
  const app = express()
  app.use(errorMiddleware)
  app.use(sessionMiddleware)
  app.use(bodyParser.json())
  app.use('/x/sessions', sessionsRouter)

  describe('GET /x/sessions', () => {
    test('get the session (logged out)', () =>
      request(app)
        .get('/x/sessions')
        .expect(res => expect(res.text).toMatchSnapshot())
        .expect(401)
        .expect('Content-Type', /json/))

    test('get the session (logged in)', () =>
      request(app)
        .post('/x/sessions')
        .send({ name: 'doris', password: 'example1' })
        .set('Accept', /application\/json/)
        .expect(200)
        .then(() =>
          request(app)
            .get('/x/sessions')
            .expect(res => expect(res.text).toMatchSnapshot())
            .expect(200)
            .expect('Content-Type', /json/)
        ))
  })

  // Order changed so that when we 'get' the session we're already logged in.
  describe('POST /x/sessions', () => {
    test('create a session (log in)', () =>
      request(app)
        .post('/x/sessions')
        .send({ name: 'doris', password: 'example1' })
        .set('Accept', /application\/json/)
        .expect(res => expect(res.text).toMatchSnapshot())
        .expect(200)
        .expect('Content-Type', /json/))
  })

  describe('PUT /x/sessions', () => {
    test('update a session -- choose a subject', () =>
      request(app)
        .put('/x/sessions')
        .send({ subject: 'd8212158-09e9-40b7-80af-4a0c014f42ba' })
        .set('Accept', /application\/json/)
        .expect(res => expect(res.text).toMatchSnapshot())
        .expect(200)
        .expect('Content-Type', /json/))

    test('update a session -- choose a unit', () =>
      request(app)
        .put('/x/sessions')
        .send({ unit: '1588ae27-86a6-4158-9d7d-2cf15c136b83' })
        .set('Accept', /application\/json/)
        .expect(res => expect(res.text).toMatchSnapshot())
        .expect(200)
        .expect('Content-Type', /json/))
  })

  describe('DELETE /x/sessions', () => {
    test('delete a session (log out)', () =>
      request(app)
        .del('/x/sessions')
        .set('Accept', /application\/json/)
        .expect(res => expect(res.text).toMatchSnapshot())
        .expect(200)
        .expect('Content-Type', /json/))
  })
})
