const Joi = require('joi')
const request = require('supertest')
const { app } = require('../index')
const {
  GQL: { getAnonymousToken },
} = require('./_util')

describe('get-anonymous-token', () => {
  it('should get an anonymous token', () =>
    request(app)
      .post('/graphql')
      .send({
        query: getAnonymousToken,
        variables: {},
      })
      .expect(({ body }) =>
        Joi.assert(
          body,
          Joi.object({
            data: Joi.object({
              anonymousToken: Joi.object({
                jwtToken: Joi.string().required(),
              }),
            }),
          })
        )
      ))
})
