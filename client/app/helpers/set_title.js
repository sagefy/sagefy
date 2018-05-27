// Set the page title.
module.exports = function setTitle(title = 'FIX ME') {
  title = `${title} – Sagefy`
  if (typeof document !== 'undefined' && document.title !== title) {
    document.title = title
  }
}
