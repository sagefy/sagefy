const broker = require('../../helpers/broker')
const tasks = require('../../helpers/tasks')

module.exports = broker.add({
  'click .my-subjects__engage-subject'(e) {
    if (e) {
      e.preventDefault()
    }
    const entityID = e.target.id
    tasks.chooseSubject(entityID)
  },
})
