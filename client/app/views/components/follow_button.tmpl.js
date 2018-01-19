const { a, p } = require('../../modules/tags')
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
