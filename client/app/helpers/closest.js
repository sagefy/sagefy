// Find the closest element matching the given selector.
module.exports = function closest(element, selector, top = document.body) {
  while (!element.matches(selector)) {
    element = element.parentNode
    if (element === top) {
      return null
    }
  }
  return element
}
