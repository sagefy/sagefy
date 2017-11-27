const tasks = {}
tasks.add = function addTasks(givenTasks) {
  Object.keys(givenTasks).forEach((key) => {
    tasks[key] = givenTasks[key]
  })
  return givenTasks
}
module.exports = tasks
