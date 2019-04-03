const Joi = require('joi')
const request = require('supertest')
const { app } = require('../index')
const {
  GQL: { rootLogInUser },
  getLoginToken,
} = require('./_util')

const success = Joi.object({
  data: Joi.object({
    logIn: Joi.object({
      jwtToken: Joi.string().required(),
    }),
  }),
})

const fail = Joi.object({
  errors: Joi.array().min(1),
  data: Joi.object({
    logIn: Joi.valid(null).required(),
  }),
})

describe('root-log-in-user', () => {
  it('should log in a user by name', () =>
    request(app)
      .post('/graphql')
      .send({
        query: rootLogInUser,
        variables: {
          name: 'Doris',
          password: 'example1',
        },
      })
      .expect(({ body }) => Joi.assert(body, success)))

  it('should log in a user by email', () =>
    request(app)
      .post('/graphql')
      .send({
        query: rootLogInUser,
        variables: {
          name: 'esther@example.com',
          password: 'example1',
        },
      })
      .expect(({ body }) => Joi.assert(body, success)))

  it('should error if no user found', () =>
    request(app)
      .post('/graphql')
      .send({
        query: rootLogInUser,
        variables: {
          name: 'riley@example.com',
          password: 'example1',
        },
      })
      .expect(({ body }) => Joi.assert(body, fail)))

  it('should error if password does not match', () =>
    request(app)
      .post('/graphql')
      .send({
        query: rootLogInUser,
        variables: {
          name: 'doris@example.com',
          password: '1elpmaxe',
        },
      })
      .expect(({ body }) => Joi.assert(body, fail)))

  it('should trim the input name/email', () =>
    request(app)
      .post('/graphql')
      .send({
        query: rootLogInUser,
        variables: {
          name: '  esther@example.com  ',
          password: 'example1',
        },
      })
      .expect(({ body }) => Joi.assert(body, success)))

  it('should trim the input password', () =>
    request(app)
      .post('/graphql')
      .send({
        query: rootLogInUser,
        variables: {
          name: 'esther@example.com',
          password: '  example1  ',
        },
      })
      .expect(({ body }) => Joi.assert(body, success)))

  it.skip('should only be available to anonymous users', async () => {
    // TODO needs a schema update
    const token = await getLoginToken('Doris')
    return request(app)
      .post('/graphql')
      .send({
        query: rootLogInUser,
        variables: {
          name: 'Doris',
          password: 'example1',
        },
      })
      .set('Authorization', `Bearer ${token}`)
      .expect(({ body }) => Joi.assert(body, fail))
  })
})
