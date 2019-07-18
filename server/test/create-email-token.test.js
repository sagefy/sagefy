const Joi = require('joi')
const request = require('supertest')
const { app } = require('../index')
const {
  GQL: { createEmailToken },
} = require('./_util')

const success = Joi.object({
  data: Joi.object({
    sendEmailToken: Joi.object({
      clientMutationId: Joi.valid(null).required(),
    }),
  }),
})

const fail = Joi.object({
  errors: Joi.array().min(1),
  data: Joi.object({
    sendEmailToken: Joi.valid(null).required(),
  }),
})

describe('create-email-token', () => {
  it('should error if no user with that email', () =>
    request(app)
      .post('/graphql')
      .send({
        query: createEmailToken,
        variables: {
          email: 'henry@example.com',
        },
      })
      .expect(({ body }) => Joi.assert(body, fail)))

  it('should send an email with the token', () =>
    request(app)
      .post('/graphql')
      .send({
        query: createEmailToken,
        variables: {
          email: 'doris@example.com',
        },
      })
      .expect(({ body }) => Joi.assert(body, success))) // TODO how do I know the email sent?

  it('should trim the input email', () =>
    request(app)
      .post('/graphql')
      .send({
        query: createEmailToken,
        variables: {
          email: '  doris@example.com  ',
        },
      })
      .expect(({ body }) => Joi.assert(body, success)))
})
