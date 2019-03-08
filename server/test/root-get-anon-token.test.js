const Joi = require('joi')
const request = require('supertest')
const { app } = require('../index')
const { GQL } = require('./_util')

describe('root-get-anon-token', () => {
  it('should get an anonymous token', () =>
    request(app)
      .post('/graphql')
      .send({
        query: GQL.rootGetAnonToken,
        variables: {},
      })
      .expect(({ body }) =>
        Joi.assert(
          body,
          Joi.object({
            data: Joi.object({
              getAnonymousToken: Joi.object({
                jwtToken: Joi.string().required(),
              }),
            }),
          })
        )
      ))
})
