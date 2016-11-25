const listeners = []
let state = typeof window === 'undefined' ? {} : window.preload || {}
let reducer = () => {}
function bind(fn) { listeners.push(fn) }
function setReducer(fn) { reducer = fn }
function dispatch(action = {type: ''}) {
    state = reducer(state, action)
    listeners.forEach(fn => fn(state, action))
}
module.exports = {setReducer, bind, dispatch}
