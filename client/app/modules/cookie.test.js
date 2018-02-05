const cookie = require('../../app/modules/cookie')

describe('Cookie', () => {
  it('should parse a cookie value', () =>
    expect(cookie.read('""+"')).toEqual('" '))

  it('should get a cookie', () => {
    document.cookie = 'test=abcd;path=/;max-age=30'
    expect(cookie.get('test')).toEqual('abcd')
    cookie.unset('test')
  })

  it('should set a cookie', () => {
    cookie.set('test', 'abcd')
    expect(document.cookie).toMatch(/test=abcd/)
    cookie.unset('test')
  })

  it('should unset a cookie', () => {
    cookie.set('test', 'abcd')
    expect(document.cookie).toMatch(/test=abcd/)
    cookie.unset('test')
    expect(document.cookie).not.toMatch(/test=abcd/)
  })
})
