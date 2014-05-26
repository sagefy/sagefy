Controller = require('./base')
$ = require('jquery')
_ = require('underscore')

class PageController extends Controller
    initialize: (options) ->
        @$page = $('.page')

        if options.model
            @model = new options.model(options.modelOptions)

        @view = new options.view(_.extend({
            model: @model || null
            $region: @$page
        }, options.viewOptions))

    beforeClose: ->
        if _.isFunction(@view.close)
            @view.close()

        @view.remove()

module.exports = PageController
