/*

{
    kind
    step (find, list, form, add, create)
    selectedSubject
        id
        members
    selectedUnit
        id
        members
    subject
    units
    cards
    searchResults /// use top level instead
    myRecentSubjects
    myRecentUnits

    proposedUnit  // popped into units
}

/create
/create/subject/form  1
/create/subject/add   1
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
    if (action.type === 'CREATE_SUBJECT_DATA') {
        state = shallowCopy(state)
        state.subject = action.values
        return state
    }
    if(action.type === 'ADD_MEMBER_TO_CREATE_SUBJECT') {
        state = shallowCopy(state)
        state.subject = copy(state.subject || {})
        const members = (state.subject.members || []).slice()
        members.push({
            kind: action.kind,
            id: action.id,
            name: action.name,
            body: action.body,
        })
        state.subject.members = members
        return state
    }
    if(action.type === 'REMOVE_MEMBER_FROM_CREATE_SUBJECT') {
        state = shallowCopy(state)
        state.subject = copy(state.subject || {})
        const members = (state.subject.members || [])
            .filter(member => member.id !== action.id)
        state.subject.members = members
        return state
    }
    if(action.type === 'REMOVE_UNIT_FROM_SUBJECT') {
        state = shallowCopy(state)
        const units = copy(state.units || [])
        units.splice(action.index, 1)
        state.units = units
        return state
    }
    if(action.type === 'SET_MY_RECENT_SUBJECTS') {
        state = shallowCopy(state)
        state.myRecentSubjects = action.subjects
        return state
    }
    if(action.type === 'CREATE_CHOOSE_SUBJECT_FOR_UNITS') {
        state = shallowCopy(state)
        state.selectedSubject = {
            id: action.id,
            name: action.name,
        }
        return state
    }
    if(action.type === 'CREATE_CHOOSE_UNIT_FOR_CARDS') {
        state = shallowCopy(state)
        state.selectedUnit = {
            id: action.id,
            name: action.name,
        }
        return state
    }
    if(action.type === 'ADD_MEMBER_TO_ADD_UNITS') {
        state = shallowCopy(state)
        state.units = state.units && state.units.slice() || []
        state.units.push({
            kind: action.kind,
            id: action.id,
            name: action.name,
            body: action.body,
            require_ids: action.require_ids,
            language: action.language,
        })
        return state
    }
    if(action.type === 'STOW_PROPOSED_UNIT') {
        state = shallowCopy(state)
        state.proposedUnit = copy(state.proposedUnit || {})
        state.proposedUnit.name = action.name
        state.proposedUnit.language = action.language
        state.proposedUnit.body = action.body
        state.proposedUnit.require_ids = action.require_ids
        return state
    }
    if(action.type === 'ADD_REQUIRE_TO_PROPOSED_UNIT') {
        state = shallowCopy(state)
        state.proposedUnit = copy(state.proposedUnit || {})
        state.proposedUnit.require_ids = state.proposedUnit.require_ids || []
        state.proposedUnit.require_ids.push({
            id: action.id,
            name: action.name,
            body: action.body,
            kind: action.kind,
        })
        return state
    }
    return state
}
