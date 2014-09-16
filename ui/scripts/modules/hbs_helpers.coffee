mixins = require('./mixins')

helpers = {
    contains: (array, value, options) ->
        if array.indexOf(value) > -1
            return options.fn(this)
        return options.inverse(this)

    isnt: (a, b, options) ->
        if a isnt b
            return options.fn(this)
        return options.inverse(this)
}

module.exports = (hbs) ->
    for name, fn of helpers
        hbs.registerHelper(name, fn)
