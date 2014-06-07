BaseController = require('../../scripts/controllers/base')

describe('Base Controller', ->
    it('should be able to call initialize on construct', ->
        class XController extends BaseController
            initialize: ->
                @foo = true

        controller = new XController()
        expect(controller.foo).to.be.true
    )

    it('should remove all listeners before delete', ->
        class XController extends BaseController
            initialize: ->
                @on('ping', -> @foo = ! @foo)

        controller = new XController()
        controller.trigger('ping')
        expect(controller.foo).to.be.true
        controller.close()
        controller.trigger('ping')
        expect(controller.foo).to.be.true
    )
)
