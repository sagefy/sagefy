Adapter = require('../framework/adapter')
util = require('../framework/utilities')
aux = require('../modules/auxiliaries')

class PageAdapter extends Adapter
    constructor: (options) ->
        super
        @render()

    requireLogIn: ->
        test = not aux.isLoggedIn()
        if test
            @navigate('/log_in')
        return test

    requireLogOut: ->
        test = aux.isLoggedIn()
        if test
            @navigate('/my_sets')
        return test

    render: ->
        @page = document.querySelector('.page')
        @page.innerHTML = ''
        title = if util.isFunction(@title) then @title() else @title or 'FIX ME'
        document.title = "#{title} – Sagefy"

module.exports = PageAdapter
