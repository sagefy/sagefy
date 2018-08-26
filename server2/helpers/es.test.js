const es = require('./es')

describe('es', () => {
  test('should connect to es', done => {
    es.ping(
      {
        requestTimeout: Infinity,
      },
      error => {
        expect(error).not.toBeDefined()
        if (error) console.error(error) // eslint-disable-line
        done()
      }
    )
  })
})
