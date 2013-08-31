require.config
    paths:
        jquery: 'jquery/jquery'
        handlebars: 'handlebars/handlebars.runtime'
        templates: 'templates'
        _: 'underscore/underscore'
        backbone: 'backbone/backbone'

require [
    'handlebars'
    'templates'
    'sections/styleguide'
], ->
    true