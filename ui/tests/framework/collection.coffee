Collection = require('../../scripts/framework/collection')

describe('Collection', ->
    it('should set a list of models', ->
        c = new Collection()
        c.set([{name: 'A'}, {name: 'B'}, {name: 'C'}])
        expect(c.models[0].get('name')).to.equal('A')
        expect(c.models[1].get('name')).to.equal('B')
        expect(c.models[2].get('name')).to.equal('C')
    )

    it('should update a list of models', ->
        c = new Collection()
        c.set([{id: 'A', name: 'A'}, {id: 'B', name: 'B'}])
        expect(c.models[0].get('name')).to.equal('A')
        expect(c.models[1].get('name')).to.equal('B')
        c.set([{id: 'A', name: 'Z'}, {id: 'C', name: 'C'}])
        expect(c.models[0].get('name')).to.equal('Z')
        expect(c.models[1].get('name')).to.equal('B')
        expect(c.models[2].get('name')).to.equal('C')
    )

    it.skip('should fetch more models', ->

    )
)
