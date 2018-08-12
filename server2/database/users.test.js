const { getUserByName } = require('./users')

describe('db: users', () => {
  describe('#getUserById', () => {
    test('should getUserById', () => {
      expect(true).toBe(false)
    })
  })

  describe('#getUserByEmail', () => {
    test('should getUserByEmail', () => {
      expect(true).toBe(false)
    })
  })

  describe('#getUserByName', () => {
    test('should getUserByName', async () => {
      const user = await getUserByName('doris')
      expect(user).toMatchSnapshot()
      expect(user.name).toBe('doris')
    })

    test('should not getUserByName', async () => {
      const user = await getUserByName('fantasia')
      expect(user).toBe(null)
    })
  })

  describe('#getUser', () => {
    test('should getUser', () => {
      expect(true).toBe(false)
    })
  })

  describe('#listUsers', () => {
    test('should listUsers', () => {
      expect(true).toBe(false)
    })
  })

  describe('#listUsersByUserIds', () => {
    test('should listUsersByUserIds', () => {
      expect(true).toBe(false)
    })
  })

  describe('#insertUser', () => {
    test('should insertUser', () => {
      expect(true).toBe(false)
    })
  })

  describe('#updateUser', () => {
    test('should updateUser', () => {
      expect(true).toBe(false)
    })
  })

  describe('#updateUserPassword', () => {
    test('should updateUserPassword', () => {
      expect(true).toBe(false)
    })
  })

  describe('#anonymizeUser', () => {
    test('should anonymizeUser', () => {
      expect(true).toBe(false)
    })
  })
})
