mixins = require('../../scripts/modules/mixins')
cookie = require('../../scripts/modules/cookie')

describe('Mixins', ->
    it('should format data from an HTML form', ->
        test = document.getElementById('test')
        test.innerHTML = '''
        <form>
            <input name="name" value="Moogle" />
            <textarea name="description">Chocobo</textarea>
        </form>
        '''
        expect(mixins.formData(test.querySelector('form')))
            .to.deep.equal({
                name: "Moogle"
                description: "Chocobo"
            })
        test.innerHTML = ''
    )

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
