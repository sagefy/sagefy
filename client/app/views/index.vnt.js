const broker = require('../modules/broker')
const tasks = require('../modules/tasks')

module.exports = broker.add({
  // When we click an internal link, use `route` instead
  'click a[href^="/"]': (e, el) => {
    e.preventDefault()
    window.scrollTo(0, 0)
    tasks.route(el.pathname + el.search)
  },

  // Do nothing on empty links
  'click a[href="#"]': (e) => {
    e.preventDefault()
  },

  // Open external URLs in new windows
  'click a[href*="//"]': (e, el) => {
    el.target = '_blank'
  },
})
