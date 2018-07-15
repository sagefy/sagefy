const request = require('supertest')

const express = require('express')
const indexRoutes = require('./index')

describe('indexRoutes', () => {
  const app = indexRoutes(express())

  describe('GET /x', () => {
    test('Should send a message', () =>
      request(app)
        .get('/x')
        .expect(200)
        .expect('Content-Type', /json/)
        .expect(res => expect(res.text).toMatchSnapshot()))
  })
})
