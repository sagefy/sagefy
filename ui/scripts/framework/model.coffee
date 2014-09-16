###

###

Events = require('./events')

class Model extends Events
    attributes: {}
    fields: {}

    url: ->
        return ''

    get: (key) ->
        return @attributes[key]

    set: (key, value) ->
        if Util.isObject(key)
            @attributes = Util.extend(key)
            @trigger('change', Object.keys(key))
        else
            @attributes[key] = value
            @trigger('change', key)
        return this

    unset: (key) ->
        @attributes[key] = null
        delete @attributes[key]
        @trigger('change', key)
        return this

    fetch: ->

    sync: ->

    save: ->

    delete: ->
        return @remove()

    validate: ->

module.exports = Model
