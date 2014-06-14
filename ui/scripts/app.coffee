$ = require('jquery')
Backbone = require('backbone')
Backbone.$ = $

PrimaryRouter = require('./routers/index')
ContributorRouter = require('./routers/contributor')
Handlebars = require('hbsfy/runtime')
hbsHelpers = require('./modules/hbs_helpers')(Handlebars)

$(->
    primaryRouter = new PrimaryRouter({ $region: $('body') })
    contributorRouter = new ContributorRouter()
    Backbone.history.start({pushState: true})
)
