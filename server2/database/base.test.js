const { omit } = require('lodash')

const {
  pool,
  convertValueToUuid,
  convertValueToSlug,
  convertText,
  convertParams,
  convertRow,
  query,
  saveList,
  save,
  list,
  get,
} = require('./base')

const UUID = '92755920-39e9-b644-a38d-64c1e1702b32'
const SLUG = 'knVZIDnptkSjjWTB4XArMg'

const INSERT_USER_QUERY = `
  INSERT INTO users
  ( name,  email,  password,  settings)
  VALUES
  ($name, $email, $password, $settings)
  RETURNING *;
`

const GET_USER_QUERY = `
  SELECT * FROM users
  WHERE id = $id;
`

const DELETE_USER_QUERY = `
  DELETE FROM users
  WHERE id = $id
  RETURNING *;
`

const INSERT_USER_PARAMS = {
  name: 'geraldine',
  email: 'geraldine@example.com',
  password: '$2a$04$Ct0xAxbyVu.TtDHm7fDpGe3ixNA8gjjDM/h6Pq69FyPevlr/pd5qm',
  settings: { email_frequency: 'daily' },
}

const USER_GEN_FIELDS = ['id', 'created', 'modified']

describe('db: index (connection and utils)', () => {
  afterAll(async () => {
    await pool.end()
  })

  describe('#convertValueToUuid', () => {
    test('should id', () => {
      expect(convertValueToUuid('id', SLUG)).toBe(UUID)
    })

    test('should _id', () => {
      expect(convertValueToUuid('a_id', SLUG)).toBe(UUID)
    })

    test('should _ids', () => {
      expect(convertValueToUuid('a_ids', [SLUG])).toEqual([UUID])
    })

    test('should none', () => {
      expect(convertValueToUuid('name', SLUG)).toBe(SLUG)
    })
  })

  describe('#convertValueToSlug', () => {
    test('should id', () => {
      expect(convertValueToSlug('id', UUID)).toBe(SLUG)
    })

    test('should _id', () => {
      expect(convertValueToSlug('a_id', UUID)).toBe(SLUG)
    })

    test('should _ids', () => {
      expect(convertValueToSlug('a_ids', [UUID])).toEqual([SLUG])
    })

    test('should none', () => {
      expect(convertValueToSlug('name', UUID)).toBe(UUID)
    })
  })

  describe('#convertText', () => {
    test('should convertText', () => {
      const xquery = `
        UPDATE users
        SET name = $name, email = $email, settings = $settings
        WHERE id = $id
        RETURNING *;
      `
      const result = `
        UPDATE users
        SET name = $1, email = $2, settings = $3
        WHERE id = $4
        RETURNING *;
      `
      expect(convertText(xquery)).toBe(result)
    })
  })

  describe('#convertParams', () => {
    test('should convertParams', () => {
      const xquery = `
        UPDATE users
        SET name = $name, email = $email, settings = $settings
        WHERE id = $id
        RETURNING *;
      `
      const params = {
        name: 'xname',
        email: 'xemail',
        settings: 'xsettings',
        id: SLUG,
      }
      const result = ['xname', 'xemail', 'xsettings', UUID]
      expect(convertParams(xquery, params)).toEqual(result)
    })
  })

  describe('#convertRow', () => {
    test('should none', () => {
      expect(convertRow(null)).toBe(null)
    })

    test('should update row', () => {
      const example = {
        id: UUID,
        email: 'xemail',
      }
      const result = {
        id: SLUG,
        email: 'xemail',
      }
      expect(convertRow(example)).toEqual(result)
    })
  })

  describe('#save, #get, #query', () => {
    test('should save, get, and delete', async () => {
      const user = await save(INSERT_USER_QUERY, INSERT_USER_PARAMS)
      expect(omit(user, USER_GEN_FIELDS)).toMatchSnapshot()
      const gotUser = await get(GET_USER_QUERY, { id: user.id })
      expect(omit(gotUser, USER_GEN_FIELDS)).toMatchSnapshot()
      await query(DELETE_USER_QUERY, { id: user.id })
      const noUser = await get(GET_USER_QUERY, { id: user.id })
      expect(noUser).toMatchSnapshot()
    })
  })

  describe('#saveList, #list, #query', () => {
    test('should savelist, list, and delete', async () => {
      const users = await saveList(INSERT_USER_QUERY, INSERT_USER_PARAMS)
      expect(users.map(user => omit(user, USER_GEN_FIELDS))).toMatchSnapshot()
      const gotUsers = await list(GET_USER_QUERY, { id: users[0].id })
      expect(
        gotUsers.map(user => omit(user, USER_GEN_FIELDS))
      ).toMatchSnapshot()
      await query(DELETE_USER_QUERY, { id: users[0].id })
      const noUsers = await list(GET_USER_QUERY, { id: users[0].id })
      expect(noUsers).toMatchSnapshot()
    })
  })
})
