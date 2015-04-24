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

    it.skip('should get a model', ->

    )

    it.skip('should get all model attributes', ->

    )

    it('should fetch more models', ->
        stub = sinon.stub(Collection::, 'ajax', (options) ->
            options.done({
                apples: [{
                    id: '1'
                    kind: 'Fuji'
                }, {
                    id: '2'
                    kind: 'Honeycrisp'
                }, {
                    id: '3'
                    kind: 'Pink Lady'
                }]
            })
        )

        class C extends Collection
            url: '/apples'

            parse: (json) ->
                return json.apples

        c = new C()
        c.fetch()
        expect(stub).to.be.called
        expect(c.models).to.have.length(3)
        expect(c.models[0].attributes).to.deep.equal({id: '1', kind: 'Fuji'})
        stub.restore()
    )
)
