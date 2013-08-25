require.config
    paths:
        jquery: 'jquery/jquery'
        handlebars: 'handlebars/handlebars.runtime'
        templates: 'templates'
        backbone: 'backbone/backbone'

require [
    'handlebars'
    'templates'
    'backbone'
    'sections/styleguide'
], ->
    true