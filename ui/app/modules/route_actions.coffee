store = require('./store')

init = ->
    prev = window.onpopstate if window.onpopstate
    @data.route = window.location.pathname
    window.onpopstate = (event) =>
        prev(event) if prev
        @data.route = window.location.pathname

route = (path) ->
    if path isnt window.location.pathname
        history.pushState({}, '', path)

store.init(init)
store.add(route)

module.exports = {init, route}
