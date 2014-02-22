define [
    'jquery'
    'hbs/styleguide/index'
], ($, t) ->
    $ ->
        if window.location.pathname != '/styleguide'
            return

        document.title = 'Sagefy Style Guide and Component Library'

        $body = $ 'body'
        $body.addClass 'max-width-10'
        $body.attr 'id', 'styleguide'
        $body.html t()

        $('a[href="#"]').click ->
            false

        $('a[href*="//"]').click ->
            @target = "_blank"
