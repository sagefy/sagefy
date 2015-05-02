validations = require('../../scripts/modules/validations')

describe('Validations', ->
    it('should require a field', ->
        expect(validations.required(null)).to.be.a('string')
        expect(validations.required()).to.be.a('string')
        expect(validations.required('')).to.be.a('string')
        expect(validations.required(1)).to.be.undefined
    )

    it('should require an email address', ->
        expect(validations.email('a')).to.be.a('string')
        expect(validations.email('a@b.c')).to.be.undefined
    )

    it('should require a minimum length', ->
        expect(validations.minlength('abc', 4)).to.be.a('string')
        expect(validations.minlength('abcd', 4)).to.be.undefined
    )
)
