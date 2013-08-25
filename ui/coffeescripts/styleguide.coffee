require 'jquery'

$ ->
    document.title = 'Descovrir Style Guide and Component Library'
    $('body').addClass 'max-width-10'
    $('a[href="#"]').click ->
        false
    $('a[href*="//"]').click ->
        @target = "_blank"