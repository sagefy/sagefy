$ = require('jquery')
Backbone = require('backbone')
Backbone.$ = $

PrimaryRouter = require('./routers/index')
Handlebars = require('hbsfy/runtime')
hbsHelpers = require('./modules/hbs_helpers')(Handlebars)

$(->
    primaryRouter = new PrimaryRouter({ $region: $('body') })
    Backbone.history.start({pushState: true})
)
