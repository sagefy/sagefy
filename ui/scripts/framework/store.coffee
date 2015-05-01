###
Stores are a collection of entries. Stores are single, persistent objects
with no knowledge of views.
Schemas should be stored separate of their stores.
###

Listener = require('./listener')
validations = require('./validations')
util = require('./utilities')

class Store extends Listener
    # Overwrite the name for events.
    # Should be like `user`, `notice`, etc.
    name: 'unknown'

    # Creates a simple object to store entries.
    # Format is `{id: entry}`.
    constructor: ->
        super
        @data = {}

    # Get the entry with the provided ID, if available.
    get: (id) ->
        return @data[id] if id in @data

    ###
    Make an Ajax call given options:
    - method: one of get, post, put, delete
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
            url += if url.indexOf('?') > -1 then '&' else '?'
            url += @parameterize(util.extend(
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
                options.done(util.parseJSON(@responseText), this)
            else
                options.fail(Store::parseAjaxErrors(this), this)
        @request.onerror = ->
            options.fail(null, this)
        if options.method is 'GET'
            @request.send()
        else
            @request.send(JSON.stringify(options.data or {}))
        return @request

    # The parse function determines what to do when the response comes back
    # from the server. Overwrite per entry.
    # Use this for any sort of `get` or `list` call.
    parse: (obj) ->
        return obj

    # Validate the entry with the given ID against the schema.
    # Returns a list of errors.
    # Triggers `invalid` if errors are found.
    # Use this method for any sort of `create` or `update` call.
    validate: (id) ->
        entry = @get(id)
        errors = []
        for fieldName in (fields or Object.keys(@schema))
            for name in schema.validations
                if util.isArray(name)
                    error = validations[name[0]](entry[fieldName],
                                                 name.slice(1))
                else
                    error = validations[name](entry[fieldName])
                if error
                    errors.push({
                        name: name
                        message: error
                    })
                    break
        @trigger("#{@name} invalid", id, errors) if errors.length
        return errors

    # Convert an object to a query string for GET requests.
    parameterize: (obj) ->
        obj = util.copy(obj)
        pairs = []
        for key, value of obj
            pairs.push(
                encodeURIComponent(key) +
                '=' +
                encodeURIComponent(value)
            )
        return pairs.join('&').replace(/%20/g, '+')

    # Try to parse the errors array or just return the error text.
    parseAjaxErrors: (r) ->
        return null if not r.responseText
        errors = util.parseJSON(r.responseText)
        return errors if util.isString(errors)
        return errors.errors

module.exports = Store
