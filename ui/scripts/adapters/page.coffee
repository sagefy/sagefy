Adapter = require('../framework/adapter')
utilities = require('../modules/utilities')

class PageAdapter extends Adapter
    constructor: (options) ->
        super
        @render()

    requireLogin: ->
        test = not utilities.isLoggedIn()
        if test
            @navigate('/login')
        return test

    requireLogout: ->
        test = utilities.isLoggedIn()
        if test
            @navigate('/dashboard')
        return test

    render: ->
        @page = document.querySelector('.page')
        @page.innerHTML = ''
        title = @title or 'FIX ME'
        document.title = "#{title} – Sagefy"

module.exports = PageAdapter
