const listeners = []
let state = typeof window === 'undefined' ? {} : window.preload || {}
let reducer = () => {}
function bind(fn) { listeners.push(fn) }
function setReducer(fn) { reducer = fn }
function dispatch(action = {type: ''}) {
    state = reducer(state, action)
    listeners.forEach(fn => fn(state, action))
}
function getState() { return state }
function resetState() { state = reducer({}, {type: ''}) }
module.exports = {setReducer, bind, dispatch, getState, resetState}
