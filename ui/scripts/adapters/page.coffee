Adapter = require('../framework/adapter')

class PageAdapter extends Adapter
    constructor: (options) ->
        super
        @page = document.querySelector('.page')
        @page.innerHTML = ''
        title = @title or 'FIX ME'
        document.title = "#{title} – Sagefy"

module.exports = PageAdapter
