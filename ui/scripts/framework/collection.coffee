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

    # Get data from the server.
    # Provide options, which will in turn be sent to the URL function.
    fetch: (options) ->

    # The parse function determines what to do when the response comes back
    # from the server. Overwrite per cocllection.
    parse: (json) ->
        return json

    # The save function will POST the collection to the server.
    # Provide options, which will in turn be sent to the URL function.
    save: (options) ->

    # Validates the values of the models against their schemas.
    # Returns a list of errors.
    # Triggers `invalid` if errors are found.
    validate: ->

    ajax: Model::ajax

module.exports = Collection
