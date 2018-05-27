const validations = require('../../app/helpers/validations')

describe('Validations', () => {
  it('should require a field', () => {
    expect(typeof validations.required(null)).toBe('string')
    expect(typeof validations.required()).toBe('string')
    expect(typeof validations.required('')).toBe('string')
    expect(validations.required(1)).toBe(null)
  })

  it('should require an email address', () => {
    expect(typeof validations.email('a')).toBe('string')
    expect(validations.email('a@b.c')).toBe(null)
  })

  it('should require a minimum length', () => {
    expect(typeof validations.minlength('abc', 4)).toBe('string')
    expect(validations.minlength('abcd', 4)).toBe(null)
  })
})
