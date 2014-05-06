md = require('marked')
moment = require('moment')
mixins = require('./mixins')
Handlebars = require('hbsfy/runtime')

helpers = {
    ### NUMBERS ###

    addCommas: (num) ->
        number.toString().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,")

    toFixed: (num, digits = 0) ->
        num.toFixed(digits)

    toPrecision: (num, digits = 0) ->
        num.toPrecision(digits)

    ### DATES AND TIMES ###

    # http://momentjs.com/docs/#/displaying/format/
    dateFormat: (datetime, format) ->
        moment(datetime).format(format)

    # http://momentjs.com/docs/#/displaying/format/
    timeAgo: (datetime) ->
        moment(datetime).fromNow()

    ### STRINGS ###

    lowercase: (str) ->
        str.toLowerCase()

    uppercase: (str) ->
        str.toUpperCase()

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

        results.join(" ")

    sentencecase: (str) ->
        str.replace(/((?:\S[^\.\?\!]*)[\.\?\!]*)/g, (txt) ->
            txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase()
        )

    truncate: (str, limit, ell = '...') ->
        if str.length < limit
            return str
        str.substring(0, limit - ell.length) + ell

    markdown: (str) ->
        md(str)

    # trim:
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
        options.inverse(this)

    after: (array, count) ->
        array.slice(count)

    withAfter: (array, count, options) ->
        array = array.slice(count)
        array.reduce((memo, el) ->
            memo + options.fn(el)
        , '')

    before: (array, count) ->
        array.slice(0, -count)

    withBefore: (array, count, options) ->
        array = array.slice(0, -count)
        array.reduce((memo, el) ->
            memo + options.fn(el)
        , '')

    first: (array) ->
        array[0]

    withFirst: (array, options) ->
        options.fn(array[0])

    last: (array) ->
        array[array.length - 1]

    withLast: (array, options) ->
        options.fn(array[array.length - 1])

    join: (array, separator) ->
        array.join(separator || ' ')

    joinSentence: (array, separator) ->
        separator ||= ' and '
        switch array.length
            when 0 then ''
            when 1 then array[0]
            when 2 then array[0] + separator + array[1]
            else
                array.slice(0, array.length - 2).join(', ') +
                    separator + array[array.length - 1]

    length: (array) ->
        array.length

    empty: (array, options) ->
        if array.length == 0
            return options.fn(this)
        options.inverse(this)

    contains: (array, value, options) ->
        if array.indexOf(value) > -1
            return options.fn(this)
        options.inverse(this)

    eachIndex: (array, options) ->
        array.reduce((memo, el) ->
            options.fn({
                item: value
                index: index
            })
        , '')

    ### COMPARISIONS ###

    and: (a, b, options) ->
        if a and b
            return options.fn(this)
        options.inverse(this)

    or: (a, b, options) ->
        if a or b
            return options.fn(this)
        options.inverse(this)

    is: (a, b, options) ->
        if a is b
            return options.fn(this)
        options.inverse(this)

    isnt: (a, b, options) ->
        if a isnt b
            return options.fn(this)
        options.inverse(this)

    gt: (a, b, options) ->
        if a > b
            return options.fn(this)
        options.inverse(this)

    gte: (a, b, options) ->
        if a >= b
            return options.fn(this)
        options.inverse(this)

    lt: (a, b, options) ->
        if a < b
            return options.fn(this)
        options.inverse(this)

    lte: (a, b, options) ->
        if a <= b
            return options.fn(this)
        options.inverse(this)
}

for name, fn of helpers
    Handlebars.registerHelper(name, fn)

module.exports = helpers
