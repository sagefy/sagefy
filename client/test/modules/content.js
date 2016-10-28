const content = require('../../app/modules/content')

describe('Content', () => {
    it('should get content', () => {
        expect(content.get('required')).to.equal('Required.')
        expect(content.get('required', 'eo')).to.equal('Postulo.')
    })
})
