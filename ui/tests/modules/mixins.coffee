mixins = require('../../scripts/modules/mixins')
$ = require('jquery')
require('jquery.cookie')
Backbone = require('backbone')

describe('Mixins', ->
    before(->
        @$test = $('#test')
    )

    it('should format data from an HTML form', ->
        formHTML = '''
        <form>
            <input name="username" value="Moogle" />
        </form>
        '''
        @$test.append(formHTML)
        expect(mixins.formData(@$test.find('form')))
            .to.eql({username: "Moogle"})
        @$test.empty()
    )

    it('should parse a JSON file, and not error if not JSON', ->
        expect(mixins.parseJSON('{"a":1}')).to.eql({a: 1})
        expect(mixins.parseJSON('bowling')).to.equal('bowling')
    )

    it('should detect login', ->
        $.cookie('logged_in', '1', {expires: 7, path: '/'})
        expect(mixins.isLoggedIn()).to.be.true
        $.cookie('logged_in', '0', {expires: 7, path: '/'})
        expect(mixins.isLoggedIn()).to.be.false
    )

    it('should parse an Ajax error', ->
        expect(mixins.parseAjaxError({responseText: '{"errors":[]}'}))
            .to.eql([])
        expect(mixins.parseAjaxError({responseText: 'crepe'}))
            .to.equal('crepe')
    )

    it('should validate email addresses', ->
        expect(mixins.validEmail('a@z.b')).to.be.true
        expect(mixins.validEmail('voo')).to.be.false
    )

    it('should validate field data', ->
        field = {name: 'username', validations: {required: true}}
        expect(mixins.validateField(field, '')).to.be.an('object')
        expect(mixins.validateField(field, 'a')).to.be.false  # no error
    )

    it('should validate fields from model data', ->
        class TestModel extends Backbone.Model
            validate: mixins.validateModelFromFields
            fields: [
                {
                    name: 'password'
                    title: 'Password'
                    type: 'password'
                    description: 'Minimum 8 characters.'
                    validations: {
                        required: true
                        minlength: 8
                    }
                }
            ]
        model = new TestModel()

        expect(model.validate(model.toJSON())).to.be.an('array')
        model.set('password', 'password')
        expect(model.validate(model.toJSON())).to.be.undefined
    )

    it('should capitalize the first letter of a string', ->
        expect(mixins.ucfirst('unicorn')).to.equal('Unicorn')
    )

    it('should underscore a name', ->
        expect(mixins.underscored('hip-po potu Mus'))
            .to.equal('hip_po_potu_mus')
    )
)
