Adapter = require('../framework/adapter')
aux = require('../modules/auxiliaries')

class PageAdapter extends Adapter
    constructor: (options) ->
        super
        @render()

    requireLogin: ->
        test = not aux.isLoggedIn()
        if test
            @navigate('/login')
        return test

    requireLogout: ->
        test = aux.isLoggedIn()
        if test
            @navigate('/my_sets')
        return test

    render: ->
        @page = document.querySelector('.page')
        @page.innerHTML = ''
        title = @title or 'FIX ME'
        document.title = "#{title} – Sagefy"

module.exports = PageAdapter
