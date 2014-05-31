$ = require('jquery')
Backbone = require('backbone')
Backbone.$ = $

PrimaryRouter = require('./routers/index')
ContributorRouter = require('./routers/contributor')
hbsHelpers = require('./modules/hbs_helpers')
cookie = require('jquery.cookie')

$(->
    primaryRouter = new PrimaryRouter()
    contributorRouter = new ContributorRouter()
    Backbone.history.start({pushState: true})
)
