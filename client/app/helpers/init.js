/* eslint-disable global-require */

const { render } = require('ultradom')
const store = require('./store')
const { getState } = require('./store')
const broker = require('./broker')

module.exports = function init({ view, el }) {
  el.innerHTML = ''
  broker.observe(el.parentNode)
  function update() {
    return render(view(getState()), el)
  }
  update()
  store.bind(update)
}
