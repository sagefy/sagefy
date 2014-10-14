###
Models are a representation in the client of data on the server.
###

Events = require('./events')
_ = require('./utilities')
validations = require('./validations')

class Model extends Events
    fields: {}

    # Creates `attributes` to ensure they are always there
    constructor: ->
        super
        @attributes = {}

    # URL can be a string or a function
    url: ''

    # Utility method, used by `fetch` and `save`
    makeUrl: (options = {}) ->
        if _.isString(@url)
            return @url
        return @url(options)

    # Get a value from the model.
    get: (key) ->
        return @attributes[key]

    # Store the value. Can take either `key, value` or `options`.
    # Does not perform any validations.
    set: (key, value) ->
        if _.isObject(key)
            @attributes = _.extend(@attributes, key)
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
                @trigger('sync')
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
    save: (options = {}) ->
        errors = @validate(options.fields or null)
        return errors if errors.length
        return @ajax({
            method: if @get('id') then 'PUT' else 'POST'
            url: @makeUrl(options)
            data: @attributes
            done: (json) =>
                @set(@parse(json))
                @trigger('sync')
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
                @trigger('sync')
            fail: (json) =>
                @trigger('error', json)
        })

    # Validates the values of the model against the schema
    # described in the fields. Returns a list of errors
    # Triggers `invalid` if errors are found.
    validate: (fields) ->
        errors = []
        for fieldName in (fields or Object.keys(@fields))
            error = @validateField(fieldName)
            errors.push({
                name: fieldName
                message: error
            }) if error
        @trigger('invalid', errors) if errors.length
        return errors

    # Validates a specific field
    # Returns an error message or null
    validateField: (fieldName) ->
        schema = @fields[fieldName]
        for vName, vVal of schema.validations
            error = validations[vName](@get(fieldName), vVal)
            return error if error

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
        url = options.url
        if options.method is 'GET'
            url += @parameterize(_.extend(
                options.data or {}
                {_: (+new Date())}  # Cachebreaker
            ))
        @request = new XMLHttpRequest()
        @request.open(method, url, true)
        @request.setRequestHeader('X-Requested-With', 'XMLHttpRequest')
        @request.setRequestHeader(
            'Content-Type'
            'application/json; charset=UTF-8'
        )
        @request.onload = ->
            if 400 > @status >= 200
                options.done(_.parseJSON(@responseText), this)
            else
                options.fail(Model::parseAjaxErrors(this), this)
        @request.onerror = ->
            options.fail(null, this)
        if options.method is 'GET'
            @request.send()
        else
            @request.send(JSON.stringify(options.data or {}))
        return @request

    # Convert an object to a query string for GET requests
    parameterize: (obj) ->
        obj = _.copy(obj)
        pairs = []
        for key, value of obj
            pairs.push(
                encodeURIComponent(key) +
                '=' +
                encodeURIComponent(value)
            )
        return '?' + pairs.join('&').replace(/%20/g, '+')

    # Try to parse the errors array
    # Or just return the error text
    parseAjaxErrors: (r) ->
        if not r.responseText
            return null
        errors =  _.parseJSON(r.responseText)
        if _.isString(errors)
            return errors
        return errors.errors

module.exports = Model
