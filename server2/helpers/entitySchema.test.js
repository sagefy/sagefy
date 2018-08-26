const entitySchema = require('./entitySchema')

describe('entitySchema', () => {
  test('should exist', () => {
    expect(entitySchema.describe()).toMatchSnapshot()
  })
})
