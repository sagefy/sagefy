const regexparam = require('regexparam').default
const { div, main } = require('../helpers/tags')

/* eslint-disable global-require */
const routes = [
  {
    path: regexparam('/c'),
    page: require('./pages/home'),
  },
]
/* eslint-enable */

module.exports = function indexView(state, actions) {
  return div(
    { className: 'vdom' },
    main(
      routes.find(route => route.path.pattern.test('/c')).page(state, actions)
    )
    // require('./components/menu.tmpl')(menuData)
  )
}
