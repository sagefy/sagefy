const Joi = require('joi')
const request = require('supertest')
const { app } = require('../index')
const {
  GQL: { updateUser }, // id, name
  getLoginToken,
  getData,
} = require('./_util')

const success = Joi.object({
  data: Joi.object({
    updateUserById: Joi.object({
      user: Joi.object({
        id: Joi.string()
          .guid()
          .required(),
        name: Joi.string().required(),
      }),
    }),
  }),
})

const fail = Joi.object({
  errors: Joi.array().min(1),
  data: Joi.object({
    updateUserById: Joi.valid(null).required(),
  }),
})

describe('update-user', () => {
  it('should let me edit my user name', async () => {
    const data = await getData()
    const token = await getLoginToken('Doris')
    await request(app)
      .post('/graphql')
      .send({
        query: updateUser,
        variables: {
          id: data.users.doris.user_id,
          name: 'Amelia',
        },
      })
      .set('Authorization', `Bearer ${token}`)
      .expect(({ body }) => Joi.assert(body, success))
    return request(app)
      .post('/graphql')
      .send({
        query: updateUser,
        variables: {
          id: data.users.doris.user_id,
          name: 'Doris',
        },
      })
      .set('Authorization', `Bearer ${token}`)
      .expect(({ body }) => Joi.assert(body, success))
  })

  it.skip(':) should let me edit my view_subjects setting', async () => {
    expect(true).toBe(false)
  })

  it('should not allow me to edit another users name', async () => {
    const data = await getData()
    const token = await getLoginToken('Doris')
    return request(app)
      .post('/graphql')
      .send({
        query: updateUser,
        variables: {
          id: data.users.esther.user_id,
          name: 'Amelia',
        },
      })
      .set('Authorization', `Bearer ${token}`)
      .expect(({ body }) => Joi.assert(body, fail))
  })

  it.skip('should allow admins to edit another users name', async () => {
    const data = await getData()
    const token = await getLoginToken('Esther')
    await request(app)
      .post('/graphql')
      .send({
        query: updateUser,
        variables: {
          id: data.users.jasmine.user_id,
          name: 'Amelia',
        },
      })
      .set('Authorization', `Bearer ${token}`)
      .expect(({ body }) => Joi.assert(body, success))
    return request(app)
      .post('/graphql')
      .send({
        query: updateUser,
        variables: {
          id: data.users.jasmine.user_id,
          name: 'Jasmine',
        },
      })
      .set('Authorization', `Bearer ${token}`)
      .expect(({ body }) => Joi.assert(body, success))
  })

  it.skip('should update the modified column if i update the user', async () => {
    expect(true).toBe(false)
  })

  it.skip('should allow me to delete my own public record', async () => {
    expect(true).toBe(false)
  })

  it.skip('should not allow me to delete another users public record', async () => {
    expect(true).toBe(false)
  })

  it.skip('should allow admins to delete another users public', async () => {
    expect(true).toBe(false)
  })
})
