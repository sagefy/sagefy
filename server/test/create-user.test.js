const Joi = require('joi')
const request = require('supertest')
const { app } = require('../index')
const {
  GQL: { createUser },
  getLoginToken,
} = require('./_util')

const success = Joi.object({
  data: Joi.object({
    signUp: Joi.object({
      jwtToken: Joi.string().required(),
    }),
  }),
})

const fail = Joi.object({
  errors: Joi.array().min(1),
  data: Joi.object({
    signUp: Joi.valid(null).required(),
  }),
})

describe('create-user', () => {
  it('should sign up a new users', () =>
    request(app)
      .post('/graphql')
      .send({
        query: createUser,
        variables: {
          name: 'gretchen',
          email: 'gretchen@example.com',
          password: 'example1',
        },
      })
      .expect(({ body }) => Joi.assert(body, success)))

  it('should error if name not unique', () =>
    request(app)
      .post('/graphql')
      .send({
        query: createUser,
        variables: {
          name: 'Doris',
          email: 'harper@example.com',
          password: 'example1',
        },
      })
      .expect(({ body }) => Joi.assert(body, fail)))

  it('should error if email not unique', () =>
    request(app)
      .post('/graphql')
      .send({
        query: createUser,
        variables: {
          name: 'Harper',
          email: 'doris@example.com',
          password: 'example1',
        },
      })
      .expect(({ body }) => Joi.assert(body, fail)))

  it('should trim name, email, password', async () => {
    await request(app)
      .post('/graphql')
      .send({
        query: createUser,
        variables: {
          name: '  sofia  ',
          email: '  sofia@example.com  ',
          password: '  example1  ',
        },
      })
      .expect(({ body }) => Joi.assert(body, success))
    expect(typeof (await getLoginToken('sofia'))).toBe('string')
    expect(typeof (await getLoginToken('sofia@example.com'))).toBe('string')
  })

  it('should require passwords >8 char', () =>
    request(app)
      .post('/graphql')
      .send({
        query: createUser,
        variables: {
          name: 'Penelope',
          email: 'penelope@example.com',
          password: 'short',
        },
      })
      .expect(({ body }) => Joi.assert(body, fail)))

  it.skip('should encrypt the password', async () => {
    expect(true).toBe(false)
  })

  it.skip('should notify the email address', async () => {
    expect(true).toBe(false)
  })

  it('should only be available to anonymous users', async () => {
    const token = await getLoginToken('Doris')
    return request(app)
      .post('/graphql')
      .send({
        query: createUser,
        variables: {
          name: 'charlotte',
          email: 'charlotte@example.com',
          password: 'example1',
        },
      })
      .set('Authorization', `Bearer ${token}`)
      .expect(({ body }) => Joi.assert(body, fail))
  })
})
