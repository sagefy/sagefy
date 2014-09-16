###

###

Events = require('./events')

class Model extends Events
    attributes: {}
    fields: {}

    url: ->
        return ''

    get: (key) ->

    set: (key, value) ->

    unset: (key) ->

    fetch: ->

    sync: ->

    save: ->

    delete: ->
        @remove()

    validate: ->

module.exports = Model
