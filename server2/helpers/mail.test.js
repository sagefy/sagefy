const sendMail = require('./mail')
const config = require('../config')

jest.mock('nodemailer', () => ({
  createTransport: () => ({
    sendMail: () => Promise.resolve(true),
  }),
}))

describe('#sendMail', () => {
  const prevConfigTest = config.test

  afterEach(() => {
    config.test = prevConfigTest
  })

  test('should skip in test mode', async () => {
    config.test = true
    expect(await sendMail({})).toBe(undefined)
  })

  test('should send an email', async () => {
    config.test = false
    expect(await sendMail({})).toBe(true)
  })
})
