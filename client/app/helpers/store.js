module.exports = function createStore() {
  const listeners = []
  const tasks = {}
  let state = (typeof window !== 'undefined' && window.preload) || {}
  let reducer = () => {}

  function bind(fn) {
    listeners.push(fn)
  }

  function setReducer(fn) {
    reducer = fn
  }

  function dispatch(action = { type: '' }) {
    state = reducer(state, action)
    listeners.forEach(fn => fn(state, action))
  }

  function getState() {
    return state
  }

  function resetState() {
    state = reducer({}, { type: '' })
  }

  function addTasks(givenTasks) {
    Object.keys(givenTasks).forEach(key => {
      tasks[key] = givenTasks[key]
    })
    return givenTasks
  }

  function getTasks() {
    return tasks
  }

  return {
    setReducer,
    bind,
    dispatch,
    getState,
    resetState,
    addTasks,
    getTasks,
  }
}
