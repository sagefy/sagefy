Adapter = require('../framework/adapter')
utilities = require('../modules/utilities')

class PageAdapter extends Adapter
    constructor: (options) ->
        super
        if @requireLogin and not utilities.isLoggedIn()
            @navigate('/login')
        else if @requireLogout and utilities.isLoggedIn()
            @navigate('/dashboard')
        else
            @render()

    render: ->
        @page = document.querySelector('.page')
        @page.innerHTML = ''
        title = @title or 'FIX ME'
        document.title = "#{title} – Sagefy"

module.exports = PageAdapter
