$ = require('jquery')
Backbone = require('backbone')
Backbone.$ = $

PrimaryRouter = require('./router')
hbsHelpers = require('./modules/hbs_helpers')
cookie = require('jquery.cookie')

primaryRouter = new PrimaryRouter()
