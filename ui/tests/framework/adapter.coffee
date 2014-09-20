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
)
