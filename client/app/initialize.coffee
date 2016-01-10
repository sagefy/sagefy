recorder = require('./modules/recorder')
store = require('./modules/store')
init = require('./modules/init')
cookie = require('./modules/cookie')

{route} = require('./modules/route_actions')

# TODO-1 Add google analytics

# Require all tasks
require('./tasks/card')
require('./tasks/follow')
require('./tasks/form')
require('./tasks/menu')
require('./tasks/notice')
require('./tasks/post')
require('./tasks/route')
require('./tasks/search')
require('./tasks/set')
require('./tasks/topic')
require('./tasks/unit')
require('./tasks/user')
require('./tasks/user_sets')

# Require all broker events
require('./views/index.vnt')

require('./views/components/follow_button.vnt')
require('./views/components/form_field_list.vnt')
require('./views/components/form_field_select.vnt')
require('./views/components/menu.vnt')
require('./views/components/notice.vnt')
require('./views/components/notices.vnt')
require('./views/components/pagination.vnt')
require('./views/components/post.vnt')
require('./views/components/query.vnt')
require('./views/components/tree.vnt')

require('./views/pages/card_learn.vnt')
require('./views/pages/card.vnt')
require('./views/pages/choose_unit.vnt')
require('./views/pages/error.vnt')
require('./views/pages/follows.vnt')
require('./views/pages/log_in.vnt')
require('./views/pages/my_sets.vnt')
require('./views/pages/password.vnt')
require('./views/pages/post_form.vnt')
require('./views/pages/search.vnt')
require('./views/pages/set.vnt')
require('./views/pages/settings.vnt')
require('./views/pages/sign_up.vnt')
require('./views/pages/topic_form.vnt')
require('./views/pages/topic.vnt')
require('./views/pages/tree.vnt')
require('./views/pages/unit.vnt')

# Log all recorder events to the console and analytics
logAllRecorderEvents = ->
    recorder.on('all', (args...) -> console.log(args...))

# Start up the application
go = ->
    logAllRecorderEvents()
    store.init(-> @data.currentUserID = cookie.get('currentUserID'))
    route(window.location.pathname + window.location.search)
    init({
        view: require('./views/index.tmpl')
        el: document.body
    })

module.exports = {go, logAllRecorderEvents}
