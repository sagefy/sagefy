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
    if (
      cache[viewKey] &&
      incomingPropsKeys.length === cachedPropsKeys.length &&
      cachedPropsKeys.every(
        k => cache[viewKey].props[k] === incomingProps[k]
      )
    ) {
      if (log) log(true)
      return cache[viewKey].value
    }
    if (log) log(false)
    cache[viewKey] = {
      props: incomingProps,
      propKeys: incomingPropsKeys,
      value: viewFn(incomingProps),
    }
    return cache[viewKey].value
  }
}

module.exports = cachedView

/*
view be like

module.exports = cachedView((props) => {
  return div()
})
*/
