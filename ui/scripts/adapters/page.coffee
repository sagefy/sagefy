Adapter = require('../framework/adapter')
mixins = require('../modules/mixins')

class PageAdapter extends Adapter
    constructor: (options) ->
        super
        if @requireLogin and not mixins.isLoggedIn()
            @navigate('/login')
        else if @requireLogout and mixins.isLoggedIn()
            @navigate('/dashboard')
        else
            @render()

    render: ->
        @page = document.querySelector('.page')
        @page.innerHTML = ''
        title = @title or 'FIX ME'
        document.title = "#{title} – Sagefy"

module.exports = PageAdapter
