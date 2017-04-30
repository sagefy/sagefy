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
    searchResults
    body
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
    if (action.type === 'WANT_CREATE_SET') {
        return Object.assign({}, state, {
            set: action.values,
        })
    }
    return state
}
