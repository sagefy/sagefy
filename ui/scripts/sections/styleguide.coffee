require ['jquery'], ($) ->
    $ ->
        # if window.location.pathname != '/styleguide':
        #     return

        document.title = 'Descovrir Style Guide and Component Library'

        $body = $ 'body'
        $body.addClass 'max-width-10'
        $body.attr 'id', 'styleguide'
        $body.html HBS['styleguide/index']()

        $('a[href="#"]').click ->
            false

        $('a[href*="//"]').click ->
            @target = "_blank"