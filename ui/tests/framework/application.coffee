App = require('../../scripts/framework/application')
Adapter = require('../../scripts/framework/adapter')

class A extends Adapter
    url: '/foo/{id}'
class B extends Adapter
    url: '/foo'
class C extends Adapter
    url: /^(.*)$/

describe('Application', ->
    it('should store all provided adapters on create', ->
        x = new App(A, B, C)
        expect(x.Adapters).to.deep.equal([A, B, C])
        x.remove()
    )

    it('should bind all provided adapters on create', ->
        spy = sinon.spy(App::, 'bindAdapter')
        x = new App(A)
        expect(spy).to.be.called
        spy.restore()
        x.remove()
    )

    it('should call bindpopstate on create', ->
        spy = sinon.spy(App::, 'bindPopState')
        x = new App(A, B, C)
        expect(spy).to.be.called
        spy.restore()
        x.remove()
    )

    it('should set an adapter to use its `navigate` function', ->
        x = new App(A, B)
        expect(x.Adapters[0]::navigate).to.equal(x.navigate)
        x.bindAdapter(C)
        expect(C::navigate).to.equal(x.navigate)
        x.unbindAdapter(C)
        x.remove()
    )

    it('should unset an adapter\'s navigate function', ->
        x = new App(A)
        expect(A::navigate).to.equal(x.navigate)
        x.unbindAdapter(A)
        expect(A::navigate).to.not.exist
        x.remove()
    )

    it('should find an adapter, given a path', ->
        x = new App(A, B, C)
        expect(x.findAdapter('/bar')).to.equal(C)
        expect(x.findAdapter('/foo')).to.equal(B)
        expect(x.findAdapter('/foo/23')).to.equal(A)
        x.remove()
    )

    describe('navigate and route', ->
        it.skip('should do nothing if navigate ' +
                'is called with the current path', ->

        )

        it.skip('should route to a new adapter', ->

        )

        it.skip('should throw an error ' +
                'if there\'s no adapter matching the path', ->

        )

        it.skip('should remove the previous adapter on a new route', ->

        )

        it.skip('should update the URL on route', ->

        )

        it.skip('should listen to the forward/back events ' +
                'and update to match', ->

        )

        it.skip('should unbind navigate from adapters when removing the app', ->

        )
    )
)
