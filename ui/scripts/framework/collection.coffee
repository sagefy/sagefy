###
A collection is a list of models.
###

Events = require('./events')
Model = require('./model')

class Collection extends Events
    # Creates `models` to ensure they are always there
    constructor: ->
        super
        @models = []

    # URL can be a string or a function
    url: ''
    makeUrl: Model::makeUrl
    Model: Model

    # For each model provided, find a model with the same ID.
    # Update existing model if found, otherwise create a new instance
    # with the given properties.
    set: (arr) ->
        for data in arr
            model = null
            if data.id
                matches = @models.filter((m) -> return m.get('id') is data.id)
                model = if matches.length then matches[0]
            if not model
                model = new @Model()
                @models.push(model)
            model.set(data)

    # Get data from the server.
    # Provide options, which will in turn be sent to the URL function.
    fetch: (options) ->
        return @ajax({
            method: 'GET'
            url: @makeUrl(options)
            done: (json) =>
                @set(@parse(json))
                @trigger('sync')
            fail: (json) =>
                @trigger('error', json)
        })

    # The parse function determines what to do when the response comes back
    # from the server. Overwrite per collection.
    parse: (json) ->
        return json

    ajax: Model::ajax
    parameterize: Model::parameterize

module.exports = Collection
