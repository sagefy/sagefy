const mapValues = require('lodash.mapvalues')

const ALL = '*'

module.exports = function createStore(defaultState) {
  const listeners = {}
  let state = (typeof window !== 'undefined' && window.preload) || defaultState

  function getState() {
    return state
  }

  function resetState() {
    state = defaultState
    return state
  }

  function addListener(type, fn) {
    listeners[type] = listeners[type] || []
    listeners[type].push(fn)
    return fn
  }

  function addListeners(obj) {
    return mapValues(obj, (fn, type) => addListener(type, fn))
  }

  function callListeners(type, value) {
    if (type in listeners) {
      listeners[type].map(listener => listener({ type, value }))
    }
  }

  function dispatch(type, fn, value) {
    const update = fn(state, value)
    Object.assign(state, update)
    callListeners(type, value)
    callListeners(ALL, value)
    return update
  }

  function bindAction(type, fn) {
    return value => dispatch(type, fn, value)
  }

  function bindActions(actions) {
    return mapValues(actions, (fn, type) => bindAction(type, fn))
  }

  return {
    getState,
    resetState,
    addListener,
    addListeners,
    bindAction,
    bindActions,
  }
}
