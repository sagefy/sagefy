Adapter = require('../../scripts/framework/adapter')
Events = require('../../scripts/framework/events')

describe('Adapter', ->
    it('should have a default URL', ->
        a = new Adapter()
        expect(a.url).to.equal('')
    )

    it('should have a constructor', ->
        class A extends Adapter
            constructor: ->
                super()
                @a = true
        a = new A
        expect(a.events).to.be.an('object')
        expect(a.a).to.be.true
    )

    it('should have a remove function', ->
        a = new Adapter()
        expect(a.remove).to.be.a('function')
    )

    it('should be an instance of Events', ->
        expect(Adapter::).to.be.an.instanceof(Events)
    )
)
