describe('Router', ->
    it('should have a default URL', ->
        a = new Adapter()
        expect(a.url).to.equal('')
    )

    it('should have a constructor', ->
        class A extends Adapter
            constructor: ->
                super
                @a = true
        a = new A
        expect(a.events).to.be.an('object')
        expect(a.a).to.be.true
    )

    it('should convert a url string to a regexp', ->
        url1 = /.*/
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

    it('should have a remove function', ->
        a = new Adapter()
        expect(a.remove).to.be.a('function')
    )

    it('should be an instance of Events', ->
        expect(Adapter::).to.be.an.instanceof(Events)
    )

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
