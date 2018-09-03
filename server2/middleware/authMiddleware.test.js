const authMiddleware = require('./authMiddleware')

describe('#authMiddleware', () => {
  test('should allow if session user', () => {
    const next = jest.fn()
    authMiddleware({ session: { user: 'abcd1234' } }, {}, next)
    expect(next).toMatchSnapshot()
  })

  test('should fail if not session user', () => {
    const next = jest.fn()
    try {
      authMiddleware({ session: {} }, {}, next)
    } catch (e) {
      expect(e).toMatchSnapshot()
    }
    expect(next).toMatchSnapshot()
  })
})
