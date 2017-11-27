const broker = require('../../modules/broker')
const tasks = require('../../modules/tasks')

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
