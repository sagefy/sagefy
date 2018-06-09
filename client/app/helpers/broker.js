const eventRegExp = /^(\S+) (.*)$/

module.exports = function createBroker() {
  const events = {
    click: {},
    change: {},
    keyup: {},
    submit: {},
  }
  let el = null

  function add(obj) {
    Object.keys(obj).forEach(query => {
      const fn = obj[query]
      const match = query.match(eventRegExp)
      const type = match ? match[1] : query
      const selector = match ? match[2] : ''
      events[type][selector] = fn
    })
    return obj
  }

  function delegate(type) {
    return e => {
      let xel = e.target
      while (xel && xel !== el) {
        Object.keys(events[type]).forEach(selector => {
          const fn = events[type][selector]
          if (xel.matches(selector)) {
            fn(e, xel)
          }
        })
        xel = xel.parentNode
      }
    }
  }

  function observe(xel) {
    el = xel
    Object.keys(events).forEach(type => {
      el.addEventListener(type, delegate(type))
    })
  }

  return { observe, add, delegate }
}
