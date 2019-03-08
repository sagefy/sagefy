const Joi = require('joi')
const request = require('supertest')
const { app } = require('../index')
const { GQL } = require('./_util')

describe('root-new-user', () => {
  it.skip(':) should sign up a new users', () =>
    request(app)
      .post('/graphql')
      .send({
        query: GQL.rootNewUser,
        variables: {
          name: 'gretchen',
          email: 'gretchen@example.com',
          password: 'example1',
        },
      })
      .expect(({ body }) =>
        Joi.assert(
          body,
          Joi.object({
            data: Joi.object({
              signUp: Joi.object({
                jwtToken: Joi.string().required(),
              }),
            }),
          })
        )
      ))

  it.skip('should error if name not unique', () => {
    expect(true).toBe(false)
  })

  it.skip('should trim name', () => {
    expect(true).toBe(false)
  })

  it.skip('should error if email not unique', () => {
    expect(true).toBe(false)
  })

  it.skip('should trim email', () => {
    expect(true).toBe(false)
  })

  it.skip('should trim the password', () => {
    expect(true).toBe(false)
  })

  it.skip('should require passwords >8 char', () => {
    expect(true).toBe(false)
  })

  it.skip('should encrypt the password', () => {
    expect(true).toBe(false)
  })

  it.skip('should notify the email address', () => {
    expect(true).toBe(false)
  })

  it.skip('should only be available to anonymous users', () => {
    expect(true).toBe(false)
  })
})
