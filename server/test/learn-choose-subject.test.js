const Joi = require('joi')
const request = require('supertest')
const { app } = require('../index')
const {
  GQL: { learnChooseSubject },
  getLoginToken,
  getData,
} = require('./_util')

describe('learn-choose-subject', () => {
  it.skip('Requires a parent subject_id', async () => {
    expect(true).toBe(false)
  })

  it('Should not choose subjects with unmet befores', async () => {
    const token = await getLoginToken('Doris')
    const data = await getData()
    return request(app)
      .post('/graphql')
      .send({
        query: learnChooseSubject,
        variables: {
          subjectId: data.subjects.all.entity_id,
        },
      })
      .set('Authorization', `Bearer ${token}`)
      .expect(({ body }) => {
        Joi.assert(
          body,
          Joi.object({
            data: Joi.object({
              selectSubjectToLearn: Joi.object({
                nodes: Joi.array()
                  .items(
                    Joi.object({
                      entityId: Joi.string()
                        .guid()
                        .required(),
                      name: Joi.string().required(),
                      body: Joi.string().required(),
                    })
                  )
                  .required(),
              }),
            }),
          })
        )
        expect(
          body.data.selectSubjectToLearn.nodes.map(({ name }) => name)
        ).toMatchSnapshot()
      })
  })

  it.skip('Should not choose subjects with no direct cards', async () => {
    expect(true).toBe(false)
  })

  it.skip('Should order subjects by depth of afters', async () => {
    expect(true).toBe(false)
  })

  it.skip('Should limit to 5 options', async () => {
    expect(true).toBe(false)
  })

  it.skip('Should do nothing if complete', async () => {
    expect(true).toBe(false)
  })

  it.skip('Can choose itself if direct cards and no child subjects', () => {
    expect(true).toBe(false)
  })
})
