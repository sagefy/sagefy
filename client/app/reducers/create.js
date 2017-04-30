/*

{
    kind
    step (find, list, form, add, create)
    selectedSet
        id
        members
    selectedUnit
        id
        members
    set
    units
    cards
    searchResults /// use top level instead
}

/create
/create/set/form  1
/create/set/add   1
-> topic/proposal
/create/unit/find 1
/create/unit/list 2
/create/unit/add  2
/create/unit/create 2
-> topic/proposal
/create/card/find 1
/create/card/list 2
/create/card/create 2
-> topic/proposal
*/
const {shallowCopy, copy} = require('../modules/utilities')

module.exports = function create(state = {}, action = {type: ''}) {
    if (action.type === 'RESET_CREATE') {
        return {}
    }
    if (action.type === 'UPDATE_CREATE_ROUTE') {
        return Object.assign({}, state, {
            kind: action.kind,
            step: action.step,
        })
    }
    if (action.type === 'CREATE_SET_DATA') {
        state = shallowCopy(state)
        state.set = action.values
        return state
    }
    if(action.type === 'ADD_MEMBER_TO_CREATE_SET') {
        state = shallowCopy(state)
        state.set = copy(state.set || {})
        const members = (state.set.members || []).slice()
        members.push({
            kind: action.kind,
            id: action.id,
            name: action.name,
            body: action.body,
        })
        state.set.members = members
        return state
    }
    return state
}
