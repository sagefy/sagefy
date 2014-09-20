###
Models are a representation in the client of data on the server.
###

# TODO: Write tests

Events = require('./events')
_ = require('./utilities')
validations = require('./validations')

class Model extends Events
    fields: {}

    # Creates `attributes` to ensure they are always there
    constructor: ->
        super()
        attributes = {}

    # URL can be a string or a function
    url: ''

    # Utility method, used by `fetch` and `save`
    makeUrl: (options) ->
        if _.isString(@url)
            return @url
        return @url(options)

    # Get a value from the model.
    get: (key) ->
        return @attributes[key]

    # Store the value. Can take either `key, value` or `options`.
    # Does not perform any validations.
    set: (key, value) ->
        if Util.isObject(key)
            @attributes = Util.extend(key)
            @trigger('change', Object.keys(key))
        else
            @attributes[key] = value
            @trigger('change', key)
        return this

    # Remove a value from the attributes.
    unset: (key) ->
        if not key
            keys = Object.keys(@attributes)
            @attributes = {}
            @trigger('change', keys)
        else
            @attributes[key] = null
            delete @attributes[key]
            @trigger('change', key)
        return this

    # Get data from the server.
    # Provide options, which will in turn be sent to the URL function.
    fetch: (options) ->
        return @ajax({
            method: 'GET'
            url: @makeUrl(options)
            done: (json) =>
                @set(@parse(json))
            fail: (json) =>
                @trigger('error', json)
        })

    # The parse function determines what to do when the response comes back
    # from the server. Overwrite per model.
    parse: (json) ->
        return json

    # The save function will either PUT or POST the model to the server,
    # depending on if the model has an ID.
    # Provide options, which will in turn be sent to the URL function.
    save: (options) ->
        errors = @validate()
        return errors if errors.length
        return @ajax({
            method: if @get('id') then 'PUT' else 'POST'
            url: @makeUrl(options)
            data: @attributes
            done: (json) =>
                @set(@parse(json))
            fail: (json) =>
                @trigger('error', json)
        })

    # Calls DELETE on the server.
    # Fails if the model has no ID.
    # Provide options, which will in turn be sent to the URL function.
    delete: (options) ->
        return false if not @get('id')
        return @ajax({
            method: 'DELETE'
            url: @makeUrl(options)
            done: =>
                @unset()
            fail: (json) =>
                @trigger('error', json)
        })

    # Validates the values of the model against the schema
    # described in the fields. Returns a list of errors
    # Triggers `invalid` if errors are found.
    validate: ->
        errors = []
        for fieldName, schema of @fields
            for vName, vVal of schema.validations
                error = validations[vName](@get(fieldName), vVal)
                errors.push(error) if errors
        @trigger('invalid', errors) if errors.length
        return errors

    ###
    Make an Ajax call given options:
    - method: one of get, post, put, patch, delete
    - url: string URL
    - data: data to send to the server
    - done: a function to do on success
        - (json, request) ->
    - fail: a function to do on fail
        - (json, request) ->
    ###
    ajax: (options) ->
        method = options.method.toUpperCase()
        if options.method is 'GET'
            url = options.url + '?_=' + (+new Date())
        else
            url = options.url
        @request = new XMLHttpRequest()
        @request.setRequestHeader('X-Requested-With', 'XMLHttpRequest')
        @request.setRequestHeader(
            'Content-Type'
            'application/json; charset=UTF-8'
        )
        @request.onload = ->
            if 400 > @status >= 200
                options.done(JSON.parse(@responseText), this)
            else
                options.fail(JSON.parse(@responseText), this)
        @request.onerror = ->
            options.fail(null, this)
        @request.open(method, url, true)
        @request.send(JSON.stringify(options.data or {}))
        return @request

module.exports = Model
