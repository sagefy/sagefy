const { convertToUuid, convertToSlug, generateSlug } = require('./uuidSlug')

describe('uuidSlug', () => {
  describe('#convertToUuid', () => {
    test('convert a slug to uuid', () => {
      expect(convertToUuid('knVZIDnptkSjjWTB4XArMg')).toBe(
        '92755920-39e9-b644-a38d-64c1e1702b32'
      )
    })

    test('leave a uuid alone', () => {
      expect(convertToUuid('669D02FA-5D77-4454-955A-C1C9531B96BA')).toBe(
        '669D02FA-5D77-4454-955A-C1C9531B96BA'
      )
    })
  })

  describe('#convertToSlug', () => {
    test('convert a uuid to a slug', () => {
      expect(convertToSlug('669D02FA-5D77-4454-955A-C1C9531B96BA')).toBe(
        'Zp0C-l13RFSVWsHJUxuWug'
      )
    })

    test('leave a slug alone', () => {
      expect(convertToSlug('knVZIDnptkSjjWTB4XArMg')).toBe(
        'knVZIDnptkSjjWTB4XArMg'
      )
    })
  })

  describe('#generateSlug', () => {
    test('generate a new uuid based slug', () => {
      expect(generateSlug()).toMatch(/^[a-zA-Z0-9_-]{22}$/)
    })
  })
})
