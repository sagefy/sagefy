const Joi = require('joi')
const request = require('supertest')
const { app } = require('../index')
const {
  GQL: { createPasswordToken },
} = require('./_util')

const success = Joi.object({
  data: Joi.object({
    sendPasswordToken: Joi.object({
      clientMutationId: Joi.valid(null).required(),
    }),
  }),
})

const fail = Joi.object({
  errors: Joi.array().min(1),
  data: Joi.object({
    sendPasswordToken: Joi.valid(null).required(),
  }),
})

describe('create-password-token', () => {
  it('should error if no user with that email', () =>
    request(app)
      .post('/graphql')
      .send({
        query: createPasswordToken,
        variables: {
          email: 'henry@example.com',
        },
      })
      .expect(({ body }) => Joi.assert(body, fail)))

  it('should send an email with the token', () =>
    request(app)
      .post('/graphql')
      .send({
        query: createPasswordToken,
        variables: {
          email: 'doris@example.com',
        },
      })
      .expect(({ body }) => Joi.assert(body, success))) // TODO how do I know the email sent?

  it('should trim the input email', () =>
    request(app)
      .post('/graphql')
      .send({
        query: createPasswordToken,
        variables: {
          email: '  doris@example.com  ',
        },
      })
      .expect(({ body }) => Joi.assert(body, success)))
})
