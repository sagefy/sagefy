Adapter = require('../framework/adapter')
_ = require('../framework/utilities')
$ = require('jquery')

class PageAdapter extends Adapter
    constructor: (options) ->
        super

        $page = $('.page')
        $page.empty()

        if @Model
            @model = new @Model(@modelOptions or {})
        if @View
            @view = new @View(_.extend({
                model: @model or null
                $region: $page
            }, @viewOptions or {}))

    remove: ->
        if _.isFunction(@view.close)
            @view.close()
        if @view
            @view.remove()
        super

module.exports = PageAdapter
