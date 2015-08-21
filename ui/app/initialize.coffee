mediator = require('./modules/mediator')

# Require all actions
require('./actions/card')
require('./actions/follow')
require('./actions/notice')
require('./actions/post')
require('./actions/search')
require('./actions/set')
require('./actions/topic')
require('./actions/unit')
require('./actions/user')

# Require all broker events

# Log all mediator events to the console and analytics
logAllMediatorEvents = ->
    mediator.on('all', (args...) -> console.log(args...))

# Start up the application
go = ->
    logAllMediatorEvents()

module.exports = {go, logAllMediatorEvents}
