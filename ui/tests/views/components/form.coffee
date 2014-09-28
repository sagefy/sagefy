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

)
