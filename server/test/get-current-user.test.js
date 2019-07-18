const Joi = require('joi')
const request = require('supertest')
const { app } = require('../index')
const {
  GQL: { getCurrentUser },
  getLoginToken,
} = require('./_util')

const success = Joi.object({
  data: Joi.object({
    getCurrentUser: Joi.object({
      id: Joi.string()
        .guid()
        .required(),
      name: Joi.string().required(),
    }),
  }),
})

const fail = Joi.object({
  data: Joi.object({
    getCurrentUser: Joi.valid(null).required(),
  }),
})

describe('get-current-user', () => {
  it('should get the current user if logged in', async () => {
    const token = await getLoginToken('Doris')
    return request(app)
      .post('/graphql')
      .send({
        query: getCurrentUser,
        variables: {},
      })
      .set('Authorization', `Bearer ${token}`)
      .expect(({ body }) => Joi.assert(body, success))
  })

  it('should get nothing if not logged in', () =>
    request(app)
      .post('/graphql')
      .send({
        query: getCurrentUser,
        variables: {},
      })
      .expect(({ body }) => Joi.assert(body, fail)))
})
