const Joi = require('joi')
const request = require('supertest')
const { app } = require('../index')
const {
  GQL: { getCardLearn },
  getData,
} = require('./_util')

const success = Joi.object({
  data: Joi.object({
    cardByEntityId: Joi.object({
      entityId: Joi.string()
        .guid()
        .required(),
      name: Joi.string().required(),
      kind: Joi.string().required(),
      data: Joi.object(),
    }),
    subjectByEntityId: Joi.object({
      learned: Joi.number().required(),
    }),
  }),
})

const fail = Joi.object({
  data: Joi.object({
    cardByEntityId: Joi.valid(null).required(),
  }),
})

describe('get-card-learn', () => {
  it('should allow anyone to read the data', async () => {
    const data = await getData()
    return request(app)
      .post('/graphql')
      .send({
        query: getCardLearn,
        variables: {
          cardId: data.cards.video.params.entity_id,
          subjectId: data.subjects.all.entity_id,
        },
      })
      .expect(({ body }) => Joi.assert(body, success))
  })

  it('should allow anyone to read the data', async () => {
    const data = await getData()
    request(app)
      .post('/graphql')
      .send({
        query: getCardLearn,
        variables: {
          cardId: '29c8ef2c-ef6b-4690-af24-e0fdf9bd30f4',
          subjectId: data.subjects.all.entity_id,
        },
      })
      .expect(({ body }) => Joi.assert(body, fail))
  })
})
