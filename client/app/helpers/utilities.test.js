const _ = require('../../app/helpers/utilities')

describe('Utilities', () => {
  it('should parse a JSON file, and not error if not JSON', () => {
    expect(_.parseJSON('{"a":1}')).toEqual({ a: 1 })
    expect(_.parseJSON('bowling')).toEqual('bowling')
  })
})
