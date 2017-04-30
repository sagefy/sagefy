const {dispatch, bind, setReducer} = require('./store')
const reducer = require('../reducers/index')
const init = require('./init')
const cookie = require('./cookie')
const {route} = require('./route_actions')
const {startGoogleAnalytics, trackEvent} = require('./analytics')
const indexView = require('../views/index.tmpl')
const {setTitle} = require('../modules/auxiliaries')

startGoogleAnalytics()

// Require all tasks
require('../tasks/card')
require('../tasks/follow')
require('../tasks/form')
require('../tasks/menu')
require('../tasks/notice')
require('../tasks/post')
require('../tasks/route')
require('../tasks/search')
require('../tasks/set')
require('../tasks/topic')
require('../tasks/unit')
require('../tasks/user')
require('../tasks/user_sets')
require('../tasks/create')

// Require all broker events
require('../views/index.vnt')

require('../views/components/follow_button.vnt')
require('../views/components/form_field_list.vnt')
require('../views/components/form_field_entities.vnt')
require('../views/components/form_field_select.vnt')
require('../views/components/menu.vnt')
require('../views/components/notice.vnt')
require('../views/components/notices.vnt')
require('../views/components/post.vnt')

require('../views/pages/card_learn.vnt')
require('../views/pages/card.vnt')
require('../views/pages/choose_unit.vnt')
require('../views/pages/error.vnt')
require('../views/pages/follows.vnt')
require('../views/pages/log_in.vnt')
require('../views/pages/my_sets.vnt')
require('../views/pages/password.vnt')
require('../views/pages/post_form.vnt')
require('../views/pages/search.vnt')
require('../views/pages/set.vnt')
require('../views/pages/settings.vnt')
require('../views/pages/sign_up.vnt')
require('../views/pages/topic_form.vnt')
require('../views/pages/topic.vnt')
require('../views/pages/tree.vnt')
require('../views/pages/unit.vnt')
require('../views/pages/create.vnt')

// Log all recorder events to the console and analytics
function logAllActions() {
    bind((state, action) => {
        console.log(action.type, action, state) // eslint-disable-line
    })
}

function trackAllActions() {
    bind((state, action) => {
        trackEvent(action)
    })
}

function updateTitle() {
    bind((state, action) => {
        if(action.type === 'SET_ROUTE') {
            setTitle(action.title)
        }
    })
}

// Start up the application
function go() {
    logAllActions()
    trackAllActions()
    updateTitle()
    setReducer(reducer)
    dispatch({
        type: 'SET_CURRENT_USER_ID',
        currentUserID: cookie.get('currentUserID'),
    })
    route(window.location.pathname + window.location.search)
    init({
        view: indexView,
        el: document.body
    })
}

module.exports = {go, logAllActions, trackAllActions}
