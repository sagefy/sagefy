/*


const { a, p } = require('../../helpers/tags')
const icon = require('./icon.tmpl')

module.exports = (kind, entityId, follows) => {
  const following = follows && follows.find(f => f.entity_id === entityId)
  return following
    ? p({ className: 'follow-button__following' }, icon('follow'), ' Following')
    : a(
        {
          id: `${kind}_${entityId}`,
          href: '#',
          className: 'follow-button',
        },
        icon('follow'),
        ' Follow'
      )
}





module.exports = (store, broker) => {
  const { getTasks } = store
  broker.add({
    'click .follow-button'(e, el) {
      if (e) {
        e.preventDefault()
      }
      const [, kind, id] = el.id.match(/^(.*?)_(.*?)$/)
      getTasks().follow({
        entity_id: id,
        entity_kind: kind,
      })
    },
  })
}




*/
