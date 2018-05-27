const broker = require('../../helpers/broker')
const tasks = require('../../helpers/tasks')

module.exports = broker.add({
  'click .follow-button'(e, el) {
    if (e) {
      e.preventDefault()
    }
    const [, kind, id] = el.id.match(/^(.*?)_(.*?)$/)
    tasks.follow({
      entity_id: id,
      entity_kind: kind,
    })
  },
})
