Utilities = require('../../scripts/framework/utilities')
extend = Utilities.extend

describe('Utilities', ->
    describe('isObject', ->
        it('should say an object is an object', ->
            expect(Utilities.isObject({})).to.be.true
        )

        it('should say a primitive is not an object', ->
            expect(Utilities.isObject(1)).to.be.false
        )

        it('should say an array is not an object', ->
            expect(Utilities.isObject([])).to.be.false
        )

        it('should say a function is not an object', ->
            expect(Utilities.isObject(->)).to.be.false
        )

        it('should say null is not an object', ->
            expect(Utilities.isObject(null)).to.be.false
            expect(Utilities.isObject(undefined)).to.be.false
        )
    )

    describe('isArray', ->
        it('should say an array is an array', ->
            expect(Utilities.isArray([])).to.be.true
        )

        it('should say an object is not an array', ->
            expect(Utilities.isArray({})).to.be.false
        )

        it('should say a primitive is not an array', ->
            expect(Utilities.isArray(1)).to.be.false
        )

        it('should say a function is not an array', ->
            expect(Utilities.isArray(->)).to.be.false
        )

        it('should say undefined or null is not an array', ->
            expect(Utilities.isArray(null)).to.be.false
        )
    )

    describe('isFunction', ->
        it('should say an array is not a function', ->
            expect(Utilities.isFunction([])).to.be.false
        )

        it('should say an object is not a function', ->
            expect(Utilities.isFunction({})).to.be.false
        )

        it('should say a primitive is not a function', ->
            expect(Utilities.isFunction(1)).to.be.false
        )

        it('should say a function is a function', ->
            expect(Utilities.isFunction(->)).to.be.true
        )

        it('should say undefined or null is not a function', ->
            expect(Utilities.isFunction(null)).to.be.false
        )
    )

    describe('isDate', ->
        it('should say a date is a date', ->
            expect(Utilities.isDate(new Date())).to.be.true
        )

        it('should say an array is not a date', ->
            expect(Utilities.isDate([])).to.be.false
        )

        it('should say an object is not a date', ->
            expect(Utilities.isDate({})).to.be.false
        )

        it('should say a primitive is not a date', ->
            expect(Utilities.isDate(1)).to.be.false
        )

        it('should say a function is not a date', ->
            expect(Utilities.isDate(->)).to.be.false
        )

        it('should say undefined or null is not a date', ->
            expect(Utilities.isDate(null)).to.be.false
        )
    )

    describe('isUndefined', ->
        it('should say undefined is undefined', ->
            expect(Utilities.isUndefined(undefined)).to.be.true
        )

        it('should say an array is not undefined', ->
            expect(Utilities.isUndefined([])).to.be.false
        )

        it('should say an object is not undefined', ->
            expect(Utilities.isUndefined({})).to.be.false
        )

        it('should say a primitive is not undefined', ->
            expect(Utilities.isUndefined(1)).to.be.false
        )

        it('should say a function is not undefined', ->
            expect(Utilities.isUndefined(->)).to.be.false
        )

        it('should say null is not undefined', ->
            expect(Utilities.isUndefined(null)).to.be.false
        )
    )

    describe('extend', ->
        it('should return identity when only one argument', ->
            a = []
            b = extend(a)
            expect(b).to.equal(a)
            a[0] = 1
            expect(b).to.have.length(1)
        )

        it('should create a duplicate object', ->
            a = {}
            b = extend({}, a)
            expect(b).to.deep.equal(a)
            a.a = 1
            expect(b).to.deep.equal({})
        )

        it('should create a duplicate array', ->
            a = []
            b = extend([], a)
            expect(b).to.deep.equal(a)
            a[0] = 1
            expect(b).to.deep.equal([])
        )

        it('should process two object injectors', ->
            a = {a: 1, b: 2, c: 3}
            b = {a: 1, b: 4, d: 5}
            c = extend({}, a, b)
            expect(a).to.deep.equal({a: 1, b: 2, c: 3})
            expect(b).to.deep.equal({a: 1, b: 4, d: 5})
            expect(c).to.deep.equal({a: 1, b: 4, c: 3, d: 5})
        )

        it('should process two array injectors', ->
            a = [1, 2, 3]
            b = [1, 4, undefined, 5]
            c = extend([], a, b)
            expect(a).to.deep.equal([1, 2, 3])
            expect(b).to.deep.equal([1, 4, undefined, 5])
            expect(c).to.deep.equal([1, 4, 3, 5])
        )

        it('should process an object and an array injector', ->
            a = {a: 1, b: 2}
            b = [1, 2]
            c = extend({}, a, b)
            expect(a).to.deep.equal({a: 1, b: 2})
            expect(b).to.deep.equal([1, 2])
            expect(c).to.deep.equal({a: 1, b: 2, 0: 1, 1: 2})
        )

        it('should process nested object injectors', ->
            a = {a: 1, b: 2, c: {a: 1}, d: {a: 1, b: 1}}
            b = {a: 1, b: {a: 1}, c: 2, d: {a: 2}}
            c = extend({}, a, b)
            expect(a).to.deep.equal({a: 1, b: 2, c: {a: 1}, d: {a: 1, b: 1}})
            expect(b).to.deep.equal({a: 1, b: {a: 1}, c: 2, d: {a: 2}})
            expect(c).to.deep.equal({a: 1, b: {a: 1}, c: 2, d: {a: 2, b: 1}})
        )

        it('should process nested array injectors', ->
            a = [0, 1, [0, 1], [0, 1, 2]]
            b = [0, [0, 1], 0, [0, 2]]
            c = extend([], a, b)
            expect(a).to.deep.equal([0, 1, [0, 1], [0, 1, 2]])
            expect(b).to.deep.equal([0, [0, 1], 0, [0, 2]])
            expect(c).to.deep.equal([0, [0, 1], 0, [0, 2, 2]])
        )

        it('should clone numbers, booleans, and strings', ->
            a = [1, 0, true, false, 'a', '']
            b = extend([], a)
            expect(b).to.deep.equal(a)
        )

        it('should ignore undefined', ->
            a = {a: undefined}
            b = extend({}, a)
            expect(b).to.deep.equal({})
        )

        it('should recognize null', ->
            a = {a: null}
            b = extend({}, a)
            expect(b).to.deep.equal({a: null})
        )

        it('should maintain references to functions', ->
            fn = ->
            a = {a: fn}
            b = {b: {a: fn}}
            c = extend({}, a, b)
            expect(c.a).to.equal(fn)
            expect(c.b.a).to.equal(fn)
        )

        it('should make copies of dates dates', ->
            d = new Date(0)  # Wed Dec 31 1969 16:00:00 GMT-0800 (PST)
            a = {a: d}
            b = {b: {a: d}}
            c = extend({}, a, b)
            expect(c.a.valueOf()).to.equal(d.valueOf())
            expect(c.b.a.valueOf()).to.equal(d.valueOf())
            c.a.setMonth(1)  # Mon Mar 03 1969 16:00:00 GMT-0800 (PST)
            expect(d.valueOf()).to.not.equal(c.a.valueOf())
        )
    )
)
