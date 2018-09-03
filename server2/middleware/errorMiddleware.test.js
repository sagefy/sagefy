const errorMiddleware = require('./errorMiddleware')
const abort = require('../helpers/abort')

function createRes() {
  return {
    status(code) {
      this.xcode = code
      return this
    },
    json(o) {
      this.xjson = o
      return this
    },
  }
}

describe('#errorMiddleware', () => {
  test('handle a status code error', () => {
    const err = abort(401)
    const req = {}
    const res = createRes()
    const next = jest.fn()
    errorMiddleware(err, req, res, next)
    expect(res).toMatchSnapshot()
    expect(next).toMatchSnapshot()
  })

  test('handle a joi validation error', () => {
    const err = {
      isJoi: true,
      details: {
        message: '"name" is not allowed to be empty',
        path: ['name'],
        type: 'any.empty',
      },
    }
    const req = {}
    const res = createRes()
    const next = jest.fn()
    errorMiddleware(err, req, res, next)
    expect(res).toMatchSnapshot()
    expect(next).toMatchSnapshot()
  })

  test('handle a 500 error', () => {
    const err = new Error()
    const req = {}
    const res = createRes()
    const next = jest.fn()
    errorMiddleware(err, req, res, next)
    expect(res).toMatchSnapshot()
    expect(next).toMatchSnapshot()
  })

  test('pass through', () => {
    const err = null
    const req = {}
    const res = createRes()
    const next = jest.fn()
    errorMiddleware(err, req, res, next)
    expect(res).toMatchSnapshot()
    expect(next).toMatchSnapshot()
  })
})
