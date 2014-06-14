BaseRouter = require('../../scripts/routers/base')
Backbone = require('backbone')

describe('Base Router', ->
    class XRouter extends BaseRouter
        routes: {
            '/notebook': 'viewNotebook'
        }
        viewNotebook: ->

    before(->
        # sinon.stub(BaseRouter::, 'beforeRoute')
        @router = new XRouter()
        Backbone.history.start({pushState: true})
    )

    after(->
        # BaseRouter::beforeRoute.restore()
        Backbone.history.stop()
        delete @router
    )

    it.skip('should call `beforeRoute` before each route', ->
        @router.navigate('/notebook', {trigger: true, replace: true})
        expect(BaseRouter::beforeRoute).to.have.been.called
        # TODO: why isn't this called?
    )

    it.skip('should close the previous controller before each route', ->
        close = sinon.spy()
        @router.controller = {close: close}
        @router.navigate('/notebook', {trigger: true, replace: true})
        expect(close).to.have.been.called
        # TODO: why isn't this called?
    )
)
