utilities = require('../../scripts/modules/utilities')
cookie = require('../../scripts/modules/cookie')

describe('Mixins', ->
    it('should detect login', ->
        cookie.set('logged_in', '1')
        expect(utilities.isLoggedIn()).to.be.true
        cookie.set('logged_in', '0')
        expect(utilities.isLoggedIn()).to.be.false
        cookie.unset('logged_in')
    )

    it('should capitalize the first letter of a string', ->
        expect(utilities.ucfirst('unicorn')).to.equal('Unicorn')
    )

    it('should underscore a name', ->
        expect(utilities.underscored('hip-po potu Mus'))
            .to.equal('hip_po_potu_mus')
    )

    it.skip('should escape HTML', ->

    )

    it.skip('should show time ago', ->

    )
)
