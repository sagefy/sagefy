// Connect a view to the state

module.exports = function connect(view) {
  return mapStateToProps => (state, actions) =>
    view(mapStateToProps(state), actions)
}
