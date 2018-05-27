const _ = require('../../app/helpers/utilities')

const { extend } = _

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

  describe('extend', () => {
    it('should return identity when only one argument', () => {
      const a = []
      const b = extend(a)
      expect(b).toEqual(a)
      a[0] = 1
      expect(b).toHaveLength(1)
    })

    it('should create a duplicate object', () => {
      const a = {}
      const b = extend({}, a)
      expect(b).toEqual(a)
      a.a = 1
      expect(b).toEqual({})
    })

    it('should create a duplicate array', () => {
      const a = []
      const b = extend([], a)
      expect(b).toEqual(a)
      a[0] = 1
      expect(b).toEqual([])
    })

    it('should process two object injectors', () => {
      const a = { a: 1, b: 2, c: 3 }
      const b = { a: 1, b: 4, d: 5 }
      const c = extend({}, a, b)
      expect(a).toEqual({ a: 1, b: 2, c: 3 })
      expect(b).toEqual({ a: 1, b: 4, d: 5 })
      expect(c).toEqual({ a: 1, b: 4, c: 3, d: 5 })
    })

    it('should process two array injectors', () => {
      const a = [1, 2, 3]
      const b = [1, 4, undefined, 5]
      const c = extend([], a, b)
      expect(a).toEqual([1, 2, 3])
      expect(b).toEqual([1, 4, undefined, 5])
      expect(c).toEqual([1, 4, 3, 5])
    })

    it('should process an object and an array injector', () => {
      const a = { a: 1, b: 2 }
      const b = [1, 2]
      const c = extend({}, a, b)
      expect(a).toEqual({ a: 1, b: 2 })
      expect(b).toEqual([1, 2])
      expect(c).toEqual({ a: 1, b: 2, 0: 1, 1: 2 })
    })

    it('should process nested object injectors', () => {
      const a = { a: 1, b: 2, c: { a: 1 }, d: { a: 1, b: 1 } }
      const b = { a: 1, b: { a: 1 }, c: 2, d: { a: 2 } }
      const c = extend({}, a, b)
      expect(a).toEqual({
        a: 1,
        b: 2,
        c: { a: 1 },
        d: { a: 1, b: 1 },
      })
      expect(b).toEqual({ a: 1, b: { a: 1 }, c: 2, d: { a: 2 } })
      expect(c).toEqual({
        a: 1,
        b: { a: 1 },
        c: 2,
        d: { a: 2, b: 1 },
      })
    })

    it('should process nested array injectors', () => {
      const a = [0, 1, [0, 1], [0, 1, 2]]
      const b = [0, [0, 1], 0, [0, 2]]
      const c = extend([], a, b)
      expect(a).toEqual([0, 1, [0, 1], [0, 1, 2]])
      expect(b).toEqual([0, [0, 1], 0, [0, 2]])
      expect(c).toEqual([0, [0, 1], 0, [0, 2, 2]])
    })

    it('should clone numbers, booleans, and strings', () => {
      const a = [1, 0, true, false, 'a', '']
      const b = extend([], a)
      expect(b).toEqual(a)
    })

    it('should ignore undefined', () => {
      const a = { a: undefined }
      const b = extend({}, a)
      expect(b).toEqual({})
    })

    it('should recognize null', () => {
      const a = { a: null }
      const b = extend({}, a)
      expect(b).toEqual({ a: null })
    })

    it('should maintain references to functions', () => {
      const fn = () => {}
      const a = { a: fn }
      const b = { b: { a: fn } }
      const c = extend({}, a, b)
      expect(c.a).toEqual(fn)
      expect(c.b.a).toEqual(fn)
    })

    it('should make copies of dates dates', () => {
      const d = new Date(0) // Wed Dec 31 1969 16:00:00 GMT-0800 (PST)
      const a = { a: d }
      const b = { b: { a: d } }
      const c = extend({}, a, b)
      expect(c.a.valueOf()).toEqual(d.valueOf())
      expect(c.b.a.valueOf()).toEqual(d.valueOf())
      c.a.setMonth(1) // Mon Mar 03 1969 16:00:00 GMT-0800 (PST)
      expect(d.valueOf()).not.toEqual(c.a.valueOf())
    })
  })

  it('should parse a JSON file, and not error if not JSON', () => {
    expect(_.parseJSON('{"a":1}')).toEqual({ a: 1 })
    expect(_.parseJSON('bowling')).toEqual('bowling')
  })
})
