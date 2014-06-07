markdown = require('marked')
moment = require('moment')
mixins = require('./mixins')

helpers = {
    ### NUMBERS ###

    addCommas: (num) ->
        return num.toString().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,")

    toFixed: (num, digits = 0) ->
        return num.toFixed(digits)

    toPrecision: (num, digits = 0) ->
        return num.toPrecision(digits)

    ### DATES AND TIMES ###

    # http://momentjs.com/docs/#/displaying/format/
    dateFormat: (datetime, format) ->
        return moment(datetime).format(format)

    # http://momentjs.com/docs/#/displaying/format/
    timeAgo: (datetime) ->
        return moment(datetime).fromNow()

    ### STRINGS ###

    lowercase: (str) ->
        return str.toLowerCase()

    uppercase: (str) ->
        return str.toUpperCase()

    ucfirst: (str) ->
        return mixins.ucfirst(str)

    titlecase: (str) ->
        title = str.replace(/[ \-_]+/g, " ")
        words = title.match(/\w+/g)
        capitalize = (word) ->
            word.charAt(0).toUpperCase() + word.slice(1)

        results = []

        for word in words
            results.push(capitalize(word))

        return results.join(" ")

    sentencecase: (str) ->
        return str.replace(/((?:\S[^\.\?\!]*)[\.\?\!]*)/g, (txt) ->
            txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase()
        )

    truncate: (str, limit, ell) ->
        if str.length < limit
            return str
        return str.substring(0, limit - ell.length) + ell

    markdown: (options) ->
        return markdown(options.fn(this))

    # trim
    # isBlank
    # stripTags
    # charLength
    # escapeHTML
    # escapeURL
    # replace
    # startsWith
    # endsWith
    # camelize
    # underscored
    # dasherize
    # humanize

    ### ARRAYS ###

    any: (array, options) ->
        if array.length
            return options.fn(this)
        return options.inverse(this)

    after: (array, count) ->
        return array.slice(count)

    withAfter: (array, count, options) ->
        array = array.slice(count)
        return array.reduce((memo, el) ->
            memo + options.fn(el)
        , '')

    before: (array, count) ->
        return array.slice(0, -count)

    withBefore: (array, count, options) ->
        array = array.slice(0, -count)
        return array.reduce((memo, el) ->
            memo + options.fn(el)
        , '')

    first: (array) ->
        return array[0]

    withFirst: (array, options) ->
        return options.fn(array[0])

    last: (array) ->
        return array[array.length - 1]

    withLast: (array, options) ->
        return options.fn(array[array.length - 1])

    join: (array, separator) ->
        return array.join(separator)

    joinSentence: (array, separator) ->
        switch array.length
            when 0 then return ''
            when 1 then return array[0]
            when 2 then return array[0] + separator + array[1]
            else
                return array.slice(0, array.length - 1).join(', ') +
                    separator + array[array.length - 1]

    length: (array) ->
        return array.length

    empty: (array, options) ->
        if array.length == 0
            return options.fn(this)
        return options.inverse(this)

    contains: (array, value, options) ->
        if array.indexOf(value) > -1
            return options.fn(this)
        return options.inverse(this)

    eachIndex: (array, options) ->
        index = -1
        return array.reduce((memo, value) ->
            index += 1
            return memo + options.fn({
                item: value
                index: index
            })
        , '')

    ### COMPARISIONS ###

    and: (a, b, options) ->
        if a and b
            return options.fn(this)
        return options.inverse(this)

    or: (a, b, options) ->
        if a or b
            return options.fn(this)
        return options.inverse(this)

    is: (a, b, options) ->
        if a is b
            return options.fn(this)
        return options.inverse(this)

    isnt: (a, b, options) ->
        if a isnt b
            return options.fn(this)
        return options.inverse(this)

    gt: (a, b, options) ->
        if a > b
            return options.fn(this)
        return options.inverse(this)

    gte: (a, b, options) ->
        if a >= b
            return options.fn(this)
        return options.inverse(this)

    lt: (a, b, options) ->
        if a < b
            return options.fn(this)
        return options.inverse(this)

    lte: (a, b, options) ->
        if a <= b
            return options.fn(this)
        return options.inverse(this)
}

module.exports = (hbs) ->
    for name, fn of helpers
        hbs.registerHelper(name, fn)
