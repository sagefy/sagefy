const bcrypt = require('bcryptjs')
const { omit } = require('lodash')

const {
  getUserById,
  getUserByEmail,
  getUserByName,
  getUser,
  listUsers,
  listUsersByUserIds,
  insertUser,
  updateUser,
  updateUserPassword,
  anonymizeUser,
} = require('./users')
const { pool, query } = require('./base')

let HELEN_ID = ''
let IRIS_ID = ''

const HELEN_DATA = {
  name: 'helen',
  email: 'helen@example.com',
  password: 'example1',
}
const IRIS_DATA = {
  name: 'iris',
  email: 'iris@example.com',
  password: 'example2',
}

const DELETE_USER_QUERY = `
  DELETE FROM users
  WHERE id = $id;
`

const GEN_PARAMS = ['id', 'created', 'modified', 'password']

const x = o => omit(o, GEN_PARAMS)

describe('db: users', () => {
  beforeAll(async () => {
    const helen = await getUserByName('helen')
    const iris = await getUserByName('iris')
    if (helen) await query(DELETE_USER_QUERY, { id: helen.id })
    if (iris) await query(DELETE_USER_QUERY, { id: iris.id })
  })

  afterAll(async () => {
    await query(DELETE_USER_QUERY, { id: HELEN_ID })
    await query(DELETE_USER_QUERY, { id: IRIS_ID })
    await pool.end()
  })

  describe('#insertUser', () => {
    test('should insertUser', async () => {
      const helen = await insertUser(HELEN_DATA)
      const iris = await insertUser(IRIS_DATA)
      expect(x(helen)).toMatchSnapshot()
      expect(x(iris)).toMatchSnapshot()
      HELEN_ID = helen.id
      IRIS_ID = iris.id
      expect(HELEN_ID).toHaveLength(22)
      expect(IRIS_ID).toHaveLength(22)
    })

    test('should fail password validation', async () => {
      try {
        await insertUser({ ...HELEN_DATA, password: 'a' })
      } catch (e) {
        expect(e.details).toMatchSnapshot()
      }
    })

    test('should fail field validation', async () => {
      try {
        await insertUser({ ...HELEN_DATA, name: '' })
      } catch (e) {
        expect(e.details).toMatchSnapshot()
      }
    })
  })

  describe('#getUserById', () => {
    test('should getUserById', async () => {
      const user = await getUserById(HELEN_ID)
      expect(x(user)).toMatchSnapshot()
      expect(user.id).toBe(HELEN_ID)
    })
  })

  describe('#getUserByEmail', () => {
    test('should getUserByEmail', async () => {
      const user = await getUserByEmail('helen@example.com')
      expect(x(user)).toMatchSnapshot()
      expect(user.email).toBe('helen@example.com')
    })
  })

  describe('#getUserByName', () => {
    test('should getUserByName', async () => {
      const user = await getUserByName('helen')
      expect(x(user)).toMatchSnapshot()
      expect(user.name).toBe('helen')
    })

    test('should not getUserByName', async () => {
      const user = await getUserByName('fantasia')
      expect(user).toBeFalsy()
    })
  })

  describe('#getUser', () => {
    test('should getUser', async () => {
      expect(x(await getUser({ id: HELEN_ID }))).toMatchSnapshot()
      expect(x(await getUser({ name: 'helen' }))).toMatchSnapshot()
      expect(
        x(await getUser({ email: 'helen@example.com' }))
      ).toMatchSnapshot()
      expect(await getUser()).toBe(null)
    })
  })

  describe('#listUsers', () => {
    test('should listUsers', async () => {
      const users = await listUsers()
      expect(users.map(x)).toMatchSnapshot()
    })
  })

  describe('#listUsersByUserIds', () => {
    test('should listUsersByUserIds', async () => {
      const users = await listUsersByUserIds([HELEN_ID, IRIS_ID])
      expect(users.map(x)).toMatchSnapshot()
    })
  })

  describe('#updateUser', () => {
    test('should updateUser', async () => {
      const user = await getUserById(HELEN_ID)
      expect(x(user)).toMatchSnapshot()
      const updatedUser = await updateUser({
        ...user,
        settings: { ...user.settings, email_frequency: 'never' },
      })
      expect(x(updatedUser)).toMatchSnapshot()
    })
  })

  describe('#updateUserPassword', () => {
    test('should updateUserPassword', async () => {
      const user = await getUserById(HELEN_ID)
      expect(await bcrypt.compare('example1', user.password)).toBe(true)
      const updatedUser = await updateUserPassword({
        id: HELEN_ID,
        password: 'example2',
      })
      expect(await bcrypt.compare('example2', updatedUser.password)).toBe(true)
    })
  })

  describe('#anonymizeUser', () => {
    test('should anonymizeUser', async () => {
      const user = await getUserById(HELEN_ID)
      expect(x(user)).toMatchSnapshot()
      await anonymizeUser(HELEN_ID)
      const updatedUser = await getUserById(HELEN_ID)
      expect(updatedUser.name).not.toBe('helen')
      expect(updatedUser.email).not.toBe('helen@example.com')
      expect(updatedUser.password).not.toBe(user.password)
    })
  })
})
