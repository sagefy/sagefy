content = require('../../app/modules/content')

describe('Content', ->
    it('should get content', ->
        expect(content.get('required')).to.equal('Required.')
        expect(content.get('required', 'eo')).to.equal('Postulo.')
    )

    it.skip('should default content to English', ->

    )

    it.skip('should show the base language if missing country-specific', ->

    )
)
