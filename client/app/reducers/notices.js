const { mergeArraysByKey } = require('../helpers/auxiliaries')
const { copy } = require('../helpers/utilities')

module.exports = function notices(state = [], action = { type: '' }) {
  if (action.type === 'LIST_NOTICES_SUCCESS') {
    const xnotices = copy(state)
    const newNotices = mergeArraysByKey(xnotices, action.notices, 'id')
    return newNotices
  }
  if (action.type === 'MARK_NOTICE_SUCCESS') {
    state.every((notice, index) => {
      if (notice.id === action.id) {
        state[index] = action.notice
      }
      return notice.id !== action.id
    })
  }
  return state
}
