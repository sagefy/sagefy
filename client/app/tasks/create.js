/* eslint-disable camelcase */
const {dispatch} = require('../modules/store')
const tasks = require('../modules/tasks')
// const request = require('../modules/request')

module.exports = tasks.add({
    resetCreate() {
        dispatch({type: 'RESET_CREATE'})
    },

    updateCreateRoute({kind, step}) {
        dispatch({type: 'UPDATE_CREATE_ROUTE', kind, step})
    },

    createSetProposal(data) {
        return tasks.createTopic(data)
    },

    createSetData(values) {
        dispatch({
            type: 'CREATE_SET_DATA',
            values,
        })
    },

    addMemberToCreateSet({kind, id, name, body}) {
        dispatch({
            type: 'ADD_MEMBER_TO_CREATE_SET',
            kind,
            id,
            name,
            body,
        })
    },

    addMemberToAddUnits({id, name, body, language = 'en', require_ids = []}) {
        dispatch({
            type: 'ADD_MEMBER_TO_ADD_UNITS',
            id,
            name,
            body,
            language,
            require_ids,
        })
    },

    removeMemberFromCreateSet({id}) {
        dispatch({
            type: 'REMOVE_MEMBER_FROM_CREATE_SET',
            id,
        })
    },

    createChooseSetForUnits({id, name}) {
        dispatch({
            type: 'CREATE_CHOOSE_SET_FOR_UNITS',
            id,
            name,
        })
    },

    stowProposedUnit({name, language, body, require_ids}) {
        dispatch({
            type: 'STOW_PROPOSED_UNIT',
            name,
            language,
            body,
            require_ids,
        })
    },

    addRequireToProposedUnit({id, name, body, kind}) {
        dispatch({
            type: 'ADD_REQUIRE_TO_PROPOSED_UNIT',
            id,
            name,
            body,
            kind
        })
    }
})
