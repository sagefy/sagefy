$ = require('jquery')
Backbone = require('backbone')
Backbone.$ = $

PrimaryRouter = require('./routers/index')
hbsHelpers = require('./modules/hbs_helpers')
cookie = require('jquery.cookie')

primaryRouter = new PrimaryRouter()
