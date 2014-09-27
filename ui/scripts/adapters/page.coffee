Adapter = require('../framework/adapter')
_ = require('../framework/utilities')

class PageAdapter extends Adapter
    constructor: (options) ->
        super

        page = document.querySelector('.page')
        page.innerHTML = ''

        if @Model
            @model = new @Model(@modelOptions or {})
        if @View
            @view = new @View(_.extend({
                model: @model or null
                region: page
            }, @viewOptions or {}))

    remove: ->
        if _.isFunction(@view.close)
            @view.close()
        if @view
            @view.remove()
        super

module.exports = PageAdapter
