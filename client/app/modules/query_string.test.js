const queryString = require('../../app/modules/query_string')

describe('Query String', () =>
  it('should parse the query string', () => {
    const qs = queryString.get('a=1&b=test&c=true&d=false&e=1.1')
    expect(qs).toEqual({
      a: 1,
      b: 'test',
      c: true,
      d: false,
      e: 1.1,
    })
  }))
