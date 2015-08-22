recorder = require('./modules/recorder')

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
require('./components/form.vnt.coffee')

# Log all recorder events to the console and analytics
logAllRecorderEvents = ->
    recorder.on('all', (args...) -> console.log(args...))

# Start up the application
go = ->
    logAllRecorderEvents()

module.exports = {go, logAllRecorderEvents}
