module.exports = function getMenuItems(kind, entityId) {
  if (!kind || !entityId)
    throw new Error('getMenuItems: Missing kind or entityId')
  return [
    {
      href: `/${kind}/${entityId}/talk`,
      icon: 'talk',
      name: 'Talk',
      itemProp: kind === 'subjects' ? 'discussionUrl' : undefined,
    },
    {
      href: `/${kind}/${entityId}/history`,
      icon: 'history',
      name: 'History',
    },
    {
      href: `/${kind}/${entityId}/edit`,
      icon: 'edit',
      name: 'Edit',
    },
  ]
}
