recorder = require('./modules/recorder')
init = require('./modules/init')

# Require all actions
require('./actions/card')
require('./actions/follow')
require('./actions/menu')
require('./actions/notice')
require('./actions/post')
require('./actions/search')
require('./actions/set')
require('./actions/topic')
require('./actions/unit')
require('./actions/user')

# Require all broker events
require('./views/index.vnt')
require('./views/components/menu.vnt')
require('./views/pages/log_in.vnt')
require('./views/pages/sign_up.vnt')

# Log all recorder events to the console and analytics
logAllRecorderEvents = ->
    recorder.on('all', (args...) -> console.log(args...))

# Start up the application
go = ->
    logAllRecorderEvents()
    init({
        view: require('./views/index.tmpl')
        el: document.body
    })

module.exports = {go, logAllRecorderEvents}
