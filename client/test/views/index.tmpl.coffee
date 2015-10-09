describe('index.tmpl', ->
    it.skip('needs tests', ->

    )
)

App = {}

###
describe.skip('Router', ->
    it('should convert a url string to a regexp', ->
        url1 = /./
        url2 = '/foo'
        url3 = '/foo/{id}'
        expect(Adapter::getUrlRegExp(url1))
            .to.equal(url1)
        expect(Adapter::getUrlRegExp(url2).toString())
            .to.equal('/^/foo$/')
        expect(Adapter::getUrlRegExp(url3).toString())
            .to.equal('/^/foo/([^/]+)$/')
    )

    it('should match a path to a regexp url', ->
        class A extends Adapter
            url: /^\/foo\/(\d+)$/

        expect(A::matches('/foo')).to.be.false
        expect(A::matches('/foo/3')).to.deep.equal(['3'])
    )

    it('should match a path to a plain string url', ->
        class A extends Adapter
            url: '/foo'

        expect(A::matches('/foo')).to.deep.equal([])
    )

    it('should match a path to a templated url string', ->
        class A extends Adapter
            url: '/foo/{id}/bar/{slug}'

        expect(A::matches('/foo')).to.be.false
        expect(A::matches('/foo/23')).to.be.false
        expect(A::matches('/foo/23/bar/52/w')).to.be.false
        expect(A::matches('/foo/23/bar/ww'))
            .to.deep.equal(['23', 'ww'])
    )

    describe.skip('navigate and route', ->
        beforeEach(->
            @paths = []
            stub = (state, title, route) => @paths.push(route)
            @pushState = sinon.stub(window.history, 'pushState', stub)
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

        it('should listen to the forward/back events ' +
                'and update to match', ->
            x = new App(A, B, C)
            x.navigate('/foo')
            x.navigate('/foo/23')
            x.navigate('/foo')
            expect(@paths).to.deep.equal([
                '/foo'
                '/foo/23'
                '/foo'
            ])
            x.remove()
        )
    )
)
###
