Form = require('../../../scripts/views/components/form')

describe('Form (Component)', ->
    it('should format data from an HTML form', ->
        form = new Form({
            region: test
        })
        form.el.innerHTML = '''
            <input name="name" value="Moogle" />
            <textarea name="description">Chocobo</textarea>
        '''
        expect(form.getValues()).to.deep.equal({
            name: "Moogle"
            description: "Chocobo"
        })
        form.remove()
    )

    it.skip('should listen to form submit', ->

    )

    it.skip('should listen to field changes', ->

    )

    it('should setup fields', ->
        f = new Form({fields: [{}]})
        expect(f.fields).to.be.an('array')
    )

    it.skip('should create the fields html', ->

    )

    it.skip('should produce a hash of values', ->

    )

    it.skip('should get a field value', ->

    )

    it.skip('should get the input fields', ->

    )

    it.skip('should get a form field wrapper', ->

    )

    it.skip('should trigger submit event', ->

    )

    it.skip('should disable submit button', ->

    )

    it.skip('should enable submit button', ->

    )

    it.skip('should debounce change events', ->

    )

    it.skip('should show a list of errors', ->

    )

    it.skip('should show an error message', ->

    )

    it.skip('should clear an error message', ->

    )

    it.skip('should clear all error messages', ->

    )
)
