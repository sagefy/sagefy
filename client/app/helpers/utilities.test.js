const _ = require('../../app/helpers/utilities')

describe('Utilities', () => {
  describe('isObject', () => {
    it('should say an object is an object', () =>
      expect(_.isObject({})).toBe(true))

    it('should say a primitive is not an object', () =>
      expect(_.isObject(1)).toBe(false))

    it('should say an array is not an object', () =>
      expect(_.isObject([])).toBe(false))

    it('should say a function is not an object', () =>
      expect(_.isObject(() => {})).toBe(false))

    it('should say null is not an object', () => {
      expect(_.isObject(null)).toBe(false)
      expect(_.isObject(undefined)).toBe(false)
    })
  })

  describe('isArray', () => {
    it('should say an array is an array', () =>
      expect(_.isArray([])).toBe(true))

    it('should say an object is not an array', () =>
      expect(_.isArray({})).toBe(false))

    it('should say a primitive is not an array', () =>
      expect(_.isArray(1)).toBe(false))

    it('should say a function is not an array', () =>
      expect(_.isArray(() => {})).toBe(false))

    it('should say undefined or null is not an array', () =>
      expect(_.isArray(null)).toBe(false))
  })

  describe('isFunction', () => {
    it('should say an array is not a function', () =>
      expect(_.isFunction([])).toBe(false))

    it('should say an object is not a function', () =>
      expect(_.isFunction({})).toBe(false))

    it('should say a primitive is not a function', () =>
      expect(_.isFunction(1)).toBe(false))

    it('should say a function is a function', () =>
      expect(_.isFunction(() => {})).toBe(true))

    it('should say undefined or null is not a function', () =>
      expect(_.isFunction(null)).toBe(false))
  })

  describe('isDate', () => {
    it('should say a date is a date', () =>
      expect(_.isDate(new Date())).toBe(true))

    it('should say an array is not a date', () =>
      expect(_.isDate([])).toBe(false))

    it('should say an object is not a date', () =>
      expect(_.isDate({})).toBe(false))

    it('should say a primitive is not a date', () =>
      expect(_.isDate(1)).toBe(false))

    it('should say a function is not a date', () =>
      expect(_.isDate(() => {})).toBe(false))

    it('should say undefined or null is not a date', () =>
      expect(_.isDate(null)).toBe(false))
  })

  describe('isUndefined', () => {
    it('should say undefined is undefined', () =>
      expect(_.isUndefined(undefined)).toBe(true))

    it('should say an array is not undefined', () =>
      expect(_.isUndefined([])).toBe(false))

    it('should say an object is not undefined', () =>
      expect(_.isUndefined({})).toBe(false))

    it('should say a primitive is not undefined', () =>
      expect(_.isUndefined(1)).toBe(false))

    it('should say a function is not undefined', () =>
      expect(_.isUndefined(() => {})).toBe(false))

    it('should say null is not undefined', () =>
      expect(_.isUndefined(null)).toBe(false))
  })

  describe('isString', () => {
    it('should say a string is a string', () =>
      expect(_.isString('')).toBe(true))

    it('should say a date is not a string', () =>
      expect(_.isString(new Date())).toBe(false))

    it('should say an array is not a string', () =>
      expect(_.isString([])).toBe(false))

    it('should say an object is not a string', () =>
      expect(_.isString({})).toBe(false))

    it('should say a number is not a string', () =>
      expect(_.isString(1)).toBe(false))

    it('should say a function is not a string', () =>
      expect(_.isString(() => {})).toBe(false))

    it('should say undefined or null is not a string', () =>
      expect(_.isString(null)).toBe(false))
  })

  describe('isRegExp', () => {
    it('should say a regexp is a regexp', () =>
      expect(_.isRegExp(/.?/)).toBe(true))

    it('should say a string is not a regexp', () =>
      expect(_.isRegExp('')).toBe(false))

    it('should say a date is not a regexp', () =>
      expect(_.isRegExp(new Date())).toBe(false))

    it('should say an array is not a regexp', () =>
      expect(_.isRegExp([])).toBe(false))

    it('should say an object is not a regexp', () =>
      expect(_.isRegExp({})).toBe(false))

    it('should say a number is not a regexp', () =>
      expect(_.isRegExp(1)).toBe(false))

    it('should say a function is not a regexp', () =>
      expect(_.isRegExp(() => {})).toBe(false))

    it('should say undefined or null is not a regexp', () =>
      expect(_.isRegExp(null)).toBe(false))
  })

  it('should parse a JSON file, and not error if not JSON', () => {
    expect(_.parseJSON('{"a":1}')).toEqual({ a: 1 })
    expect(_.parseJSON('bowling')).toEqual('bowling')
  })
})
