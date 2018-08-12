const request = require('supertest')
const express = require('express')
const indexRouter = require('./index')

describe('indexRouter', () => {
  const app = express()
  app.use('/x', indexRouter)

  describe('GET /x', () => {
    test('Should send a message', () =>
      request(app)
        .get('/x')
        .expect(200)
        .expect('Content-Type', /json/)
        .expect(res => expect(res.text).toMatchSnapshot()))
  })

  describe('GET /x/sitemap', () => {
    test('should create a sitemap', () => {
      expect(true).toBe(false)
    })
  })

  describe('GET /x/search', () => {
    test('should get search results', () => {
      expect(true).toBe(false)
    })
  })
})
