const get = require('lodash.get')
const GQL = require('./gql-queries')

describe('gql-queries', () => {
  it('should load gql queries', () => {
    Object.keys(GQL).forEach(key => {
      expect(typeof key).toBe('string')
      expect(typeof get(GQL, key)).toBe('function')
    })
  })
})
