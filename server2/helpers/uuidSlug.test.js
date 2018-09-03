const { convertToUuid, convertToSlug, generateSlug } = require('./uuidSlug')

const UUID = '92755920-39e9-b644-a38d-64c1e1702b32'
const SLUG = 'knVZIDnptkSjjWTB4XArMg'

describe('uuidSlug', () => {
  describe('#convertToUuid', () => {
    test('convert a slug to uuid', () => {
      expect(convertToUuid(SLUG)).toBe(UUID)
    })

    test('leave a uuid alone', () => {
      expect(convertToUuid(UUID)).toBe(UUID)
    })
  })

  describe('#convertToSlug', () => {
    test('convert a uuid to a slug', () => {
      expect(convertToSlug(UUID)).toBe(SLUG)
    })

    test('leave a slug alone', () => {
      expect(convertToSlug(SLUG)).toBe(SLUG)
    })
  })

  describe('#generateSlug', () => {
    test('generate a new uuid based slug', () => {
      expect(generateSlug()).toMatch(/^[a-zA-Z0-9_-]{22}$/)
    })
  })
})
