aux = require('../../scripts/modules/auxiliaries')
cookie = require('../../scripts/modules/cookie')

describe('Auxiliaries', ->
    it('should detect login', ->
        cookie.set('logged_in', '1')
        expect(aux.isLoggedIn()).to.be.true
        cookie.set('logged_in', '0')
        expect(aux.isLoggedIn()).to.be.false
        cookie.unset('logged_in')
    )

    it('should capitalize the first letter of a string', ->
        expect(aux.ucfirst('unicorn')).to.equal('Unicorn')
    )

    it('should underscore a name', ->
        expect(aux.underscored('hip-po potu Mus'))
            .to.equal('hip_po_potu_mus')
    )

    it.skip('should escape HTML', ->

    )

    it.skip('should show time ago', ->

    )
)
