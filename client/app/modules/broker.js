require('./matches_polyfill')

const eventRegExp = /^(\S+) (.*)$/

module.exports = {
  events: {
    click: {},
    change: {},
    keyup: {},
    submit: {},
  },

  init: function init(fn) {
    fn.call(this)
  },

  observe: function observer(el) {
    this.el = el
    Object.keys(this.events).forEach(type => {
      this.el.addEventListener(type, this.delegate(type))
    })
  },

  add: function add(obj) {
    Object.keys(obj).forEach(query => {
      const fn = obj[query]
      const match = query.match(eventRegExp)
      const type = match ? match[1] : query
      const selector = match ? match[2] : ''
      this.events[type][selector] = fn
    })
    return obj
  },

  delegate: function delegate(type) {
    return e => {
      let el = e.target
      while (el && el !== this.el) {
        Object.keys(this.events[type]).forEach(selector => {
          const fn = this.events[type][selector]
          if (el.matches(selector)) {
            fn.call(this, e, el)
          }
        })
        el = el.parentNode
      }
    }
  },
}
