recorder = require('./modules/recorder')
store = require('./modules/store')
init = require('./modules/init')
cookie = require('./modules/cookie')

{route} = require('./modules/route_actions')

# Require all actions
require('./actions/card')
require('./actions/follow')
require('./actions/menu')
require('./actions/notice')
require('./actions/post')
require('./actions/route')
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
require('./views/pages/password.vnt')
require('./views/pages/settings.vnt')
require('./views/components/notices.vnt')
require('./views/components/notice.vnt')

# Log all recorder events to the console and analytics
logAllRecorderEvents = ->
    recorder.on('all', (args...) -> console.log(args...))

# Start up the application
go = ->
    logAllRecorderEvents()
    store.init(-> @data.currentUserID = cookie.get('currentUserID'))
    route(window.location.pathname)
    init({
        view: require('./views/index.tmpl')
        el: document.body
    })

module.exports = {go, logAllRecorderEvents}
