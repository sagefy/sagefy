const { get, set, setex, ttl, del } = require('./redis')

describe('#redis', () => {
  test('should have get, set, and delete methods', async () => {
    expect(await get('testkey')).toBe(null)
    await set('testkey', 'hello')
    expect(await get('testkey')).toBe('hello')
    await del('testkey')
    expect(await get('testkey')).toBe(null)
  })

  test('should have setex and ttl method', async () => {
    await setex('testkey', 1, 'hello')
    expect(await get('testkey')).toBe('hello')
    expect(await ttl('testkey')).toBe(1)
    await del('testkey')
    expect(await get('testkey')).toBe(null)
  })
})
