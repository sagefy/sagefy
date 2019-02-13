import request from 'supertest'
import app from './index'

describe('index', () => {
  it('should create an app', () => {
    expect(app).not.toBe(null)
  })

  it('GET *', async () => {
    const response = await request(app).get('/')
    expect(response.statusCode).toBe(200)
  })
})
