const abort = require('./abort')

describe('#abort', () => {
  test('err with props', () => {
    expect(abort(418, 'hello')).toMatchSnapshot()
  })

  test('err with json', () => {
    expect(abort(418, 'hello', { errors: [] })).toMatchSnapshot()
  })
})
