const request = require('supertest')
const express = require('express')
const sessionsRouter = require('./sessions')

describe('Sessions Routes', () => {
  const app = express()
  app.use('/x/sessions', sessionsRouter)

  describe('GET /x/sessions', () => {
    test('get the session (logged out)', () =>
      request(app)
        .get('/x/sessions')
        .expect(200)
        .expect('Content-Type', /json/)
        .expect(res => expect(res.text).toMatchSnapshot()))

    test('get the session (logged in)', () => {
      request(app)
        .post('/x/sessions')
        .send({ name: 'doris', password: 'example1' })
        .set('Accept', /application\/json/)
        .expect(200)
      return request(app)
        .get('/x/sessions')
        .expect(200)
        .expect('Content-Type', /json/)
        .expect(res => expect(res.text).toMatchSnapshot())
    })
  })

  // Order changed so that when we 'get' the session we're already logged in.
  describe('POST /x/sessions', () => {
    test('create a session (log in)', () =>
      request(app)
        .post('/x/sessions')
        .send({ name: 'doris', password: 'example1' })
        .set('Accept', /application\/json/)
        .expect(200)
        .expect('Content-Type', /json/)
        .expect(res => expect(res.text).toMatchSnapshot()))
  })

  describe('PUT /x/sessions', () => {
    test('update a session -- choose a subject', () =>
      request(app)
        .put('/x/sessions')
        .send({ subject: 'd8212158-09e9-40b7-80af-4a0c014f42ba' })
        .set('Accept', /application\/json/)
        .expect(200)
        .expect('Content-Type', /json/)
        .expect(res => expect(res.text).toMatchSnapshot()))

    test('update a session -- choose a unit', () => {
      request(app)
        .put('/x/sessions')
        .send({ unit: '1588ae27-86a6-4158-9d7d-2cf15c136b83' })
        .set('Accept', /application\/json/)
        .expect(200)
        .expect('Content-Type', /json/)
        .expect(res => expect(res.text).toMatchSnapshot())
    })
  })

  describe('DELETE /x/sessions', () => {
    test('delete a session (log out)', () => {
      request(app)
        .delete('/x/sessions')
        .set('Accept', /application\/json/)
        .expect(200)
        .expect('Content-Type', /json/)
        .expect(res => expect(res.text).toMatchSnapshot())
    })
  })
})
