module.exports = function goLogin() {
  if (typeof window !== 'undefined') {
    window.location = '/log_in'
  }
}
