import request from 'supertest'
import app from './index'

describe('index', () => {
  it('should create an app', () => {
    expect(app).not.toBe(null)
  })

  it.skip('GET *', async () => {
    const response = await request(app).get('/')
    expect(response.statusCode).toBe(200)
  })

  it.skip('POST /sign-up', async () => {
    const response = await request(app).post('/')
    expect(response.statusCode).toBe(200)
    expect(response.text).toMatchSnapshot()
  })
})
