IndexRouter = require('../../scripts/routers/index')
$ = require('jquery')
Backbone = require('backbone')

describe('Index Router', ->
    before(->
        @$test = $('#test')
        @viewErrorStub = sinon.stub(IndexRouter::, 'viewError')
        @router = new IndexRouter({$region: @$test})
        Backbone.history.start({pushState: true})
    )

    after(->
        Backbone.history.stop()
        @viewErrorStub.restore()
        delete @router
    )

    it('should add the menu view', ->
        expect(@$test).to.have('.menu__items')
    )

    it('should create the page element', ->
        expect(@$test).to.have('.page')
    )

    it('should 404 if the URL doesn\'t match', ->
        @router.navigate('/rainbow', {trigger: true, replace: true})
        expect(@router.viewError).to.have.been.called
    )
)
