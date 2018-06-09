/* eslint-disable no-console */ /* eslint-disable global-require */

const { render } = require('ultradom')
const createStore = require('./store')
const createBroker = require('../helpers/broker')
const reducer = require('../reducers/index')
const { route, initRouting } = require('./route_actions')
const indexView = require('../views/index.tmpl')
const setTitle = require('../helpers/set_title')
const addAllTasks = require('../tasks/index')
const allAllEvents = require('../views/all.vnt')

// Log all recorder events to the console
function logAllActions(store) {
  store.bind((state, action) => {
    console.log(action.type, action, state)
  })
}

function updateTitle(store) {
  store.bind((state, action) => {
    if (action.type === 'SET_ROUTE') {
      setTitle(action.title)
    }
  })
}

function build({ view, el }) {
  const store = createStore()
  const broker = createBroker()
  store.setReducer(reducer)
  el.innerHTML = ''
  broker.observe(el.parentNode)
  function update() {
    return render(view(store.getState()), el)
  }
  update()
  store.bind(update)
  return { store, broker }
}

// Start up the application
function go() {
  const { store, broker } = build({
    view: indexView,
    el: document.querySelector('.vdom'),
  })
  addAllTasks(store)
  allAllEvents(store, broker)
  logAllActions(store)
  updateTitle(store)
  initRouting(store)
  route(store, window.location.pathname + window.location.search)
}

module.exports = { go }
