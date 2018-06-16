const { createStore } = require('redux')
const { render } = require('ultradom')

const view = require('./views/index')

const store = createStore((a = {}) => a)

document.addEventListener('DOMContentLoaded', () => {
  const el = document.querySelector('.vdom')
  el.innerHTML = ''
  function update() {
    render(view(store.getState()), el)
  }
  update()
  store.subscribe(update)
})

/* const { createStore, applyMiddleware, bindActionCreators } = require('redux')
const createReduxListen = require('redux-listen')
const { createReducer, createActions /* createActionTypes } = require('redux-schemad')
const { stateSchema } = require('./state/stateSchema')

const view = require('./views/index')

const reducer = createReducer(stateSchema)
const listenStore = createReduxListen()
const store = createStore(reducer, applyMiddleware(listenStore))
const actions = bindActionCreators(createActions(stateSchema), store.dispatch)
// const actionTypes = createActionTypes(stateSchema)

document.addEventListener('DOMContentLoaded', () => {
  const el = document.querySelector('.vdom')
  el.innerHTML = ''
  function render() {
    render(view(store.getState(), actions), el)
  }
  render()
  store.subscribe(render)
})
*/
