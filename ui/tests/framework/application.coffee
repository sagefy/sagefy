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
        expect(x.Adapters[0]::navigate).to.be.a('function')
        x.bindAdapter(C)
        expect(C::navigate).to.be.a('function')
        x.unbindAdapter(C)
        x.remove()
    )

    it('should unset an adapter\'s navigate function', ->
        x = new App(A)
        expect(A::navigate).to.be.a('function')
        x.unbindAdapter(A)
        expect(A::navigate).to.not.exist
        x.remove()
    )

    it('should unbind navigate from adapters when removing the app', ->
        x = new App(A)
        expect(A::navigate).to.be.a('function')
        x.remove()
        expect(A::navigate).to.not.exist
    )

    it('should find an adapter, given a path', ->
        x = new App(A, B, C)
        expect(x.findAdapter('/bar')).to.equal(C)
        expect(x.findAdapter('/foo')).to.equal(B)
        expect(x.findAdapter('/foo/23')).to.equal(A)
        x.remove()
    )

    describe('navigate and route', ->
        beforeEach(->
            @pushState = sinon.stub(window.history, 'pushState')
        )

        afterEach(->
            @pushState.restore()
        )

        it('should do nothing if navigate ' +
           'is called with the current path', ->
            spy = sinon.spy(App::, 'route')
            x = new App()
            x.navigate(window.location.pathname)
            expect(spy).to.not.be.called
            expect(@pushState).to.not.be.called
            x.remove()
            spy.restore()
        )

        it('should route to a new adapter', ->
            spy = sinon.spy(App::, 'route')
            x = new App(A, B, C)
            x.navigate('/foo')
            expect(spy).to.be.called
            expect(@pushState).to.be.called
            expect(x.adapter).to.be.instanceof(B)
            x.remove()
            spy.restore()
        )

        it('should throw an error ' +
           'if there\'s no adapter matching the path', ->
            x = new App(A, B)
            expect(-> x.navigate('/bar')).to.throw
            expect(@pushState).to.not.be.called
            x.remove()
        )

        it('should remove the previous adapter on a new route', ->
            x = new App(A, B, C)
            x.navigate('/foo')
            expect(x.adapter).to.be.instanceof(B)
            spy = sinon.spy(x.adapter, 'remove')
            x.navigate('/foo/23')
            expect(spy).to.be.called
            expect(x.adapter).to.be.instanceof(A)
            x.remove()
        )

        it.skip('should listen to the forward/back events ' +
                'and update to match', ->
            x = new App(A, B, C)
            x.navigate('/foo')
            x.navigate('/foo/23')
            # TODO hit back button ???
            # but we can't actually change the path
            x.remove()
        )
    )
)
