define [
    'jquery'
    'underscore'
    'hbs/public/index'
], ($, _, t) ->
    $ ->

        if ! _.contains ['', '/'], window.location.pathname
            return

        document.title = 'Sagefy - Adaptive, collaborative, and open learning platform.'

        $body = $ 'body'
        $body.addClass 'max-width-8'
        $body.attr 'id', 'index'
        $body.html t()
