// Inspects the properties of the first argument.
// If the top level hard matches, the cache response is used in place.

function cachedView(viewFn, log) {
  const cache = {}
  const defaultKey = 'default'
  return function myCachedView(incomingProps) {
    if (arguments.length !== 1) {
      throw new Error('cachedView must not receive more than props')
    }
    const viewKey = incomingProps.key || defaultKey
    const incomingPropsKeys = Object.keys(incomingProps)
    const cachedPropsKeys = cache[viewKey].propKeys
    if (cache[viewKey] &&
        incomingPropsKeys.length === cachedPropsKeys.length &&
        cachedPropsKeys.every(k => cache[viewKey].value[k] === incomingProps[k])
    ) {
      log && log(true)
      return cachedReturn
    }
    log && log(false)
    cache[viewKey] = {
      props: incomingProps,
      propKeys: incomingPropsKeys,
      value: viewFn(...arguments),
    }
    return cache[viewKey].value
  }
}


/*
view be like

module.exports = cachedView((props) => {
  return div()
})
*/
