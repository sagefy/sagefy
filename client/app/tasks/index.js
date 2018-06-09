/* eslint-disable global-require */

module.exports = function addAllTasks(store) {
  require('./card')(store)
  require('./follow')(store)
  require('./form')(store)
  require('./menu')(store)
  require('./notice')(store)
  require('./post')(store)
  require('./route')(store)
  require('./search')(store)
  require('./subject')(store)
  require('./topic')(store)
  require('./unit')(store)
  require('./user')(store)
  require('./user_subjects')(store)
  require('./create')(store)
  require('./entity')(store)
}
