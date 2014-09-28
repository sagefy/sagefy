mixins = require('../../scripts/modules/mixins')
cookie = require('../../scripts/modules/cookie')

describe('Mixins', ->
    it('should detect login', ->
        cookie.set('logged_in', '1')
        expect(mixins.isLoggedIn()).to.be.true
        cookie.set('logged_in', '0')
        expect(mixins.isLoggedIn()).to.be.false
        cookie.unset('logged_in')
    )

    it('should capitalize the first letter of a string', ->
        expect(mixins.ucfirst('unicorn')).to.equal('Unicorn')
    )

    it('should underscore a name', ->
        expect(mixins.underscored('hip-po potu Mus'))
            .to.equal('hip_po_potu_mus')
    )
)
