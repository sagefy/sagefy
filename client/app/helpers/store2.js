const mapValues = require('lodash.mapvalues')

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
    mapValues(obj, (fn, type) => addListener(type, fn))
    return obj
  }

  function dispatch(type, fn, value) {
    const update = fn(state, value)
    Object.assign(state, update)
    ;[type, '*'].forEach(
      xtype =>
        xtype in listeners &&
        listeners[xtype].forEach(listener =>
          listener({ type, value, getState })
        )
    )
    return update
  }

  function bindAction(type, fn) {
    return value => dispatch(type, fn, value)
  }

  function bindActions(actions) {
    mapValues(actions, (fn, type) => bindAction(type, fn))
  }

  return {
    getState,
    resetState,
    addListener,
    addListeners,
    dispatch,
    bindAction,
    bindActions,
  }
}
