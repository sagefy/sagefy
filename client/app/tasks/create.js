/* eslint-disable camelcase */
const {dispatch, getState} = require('../modules/store')
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

    removeUnitFromSet({index}) {
        dispatch({
            type: 'REMOVE_UNIT_FROM_SET',
            index,
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
    },

    createUnitsProposal() {
        const state = getState()
        const {selectedSet} = state.create
        const data = {
            topic: {
                name: 'Add Units to This Set',
                entity: {
                    id: selectedSet.id,
                    kind: 'set',
                },
            },
            post: {
                kind: 'proposal',
                body: 'Add Units to Set',
            }
            /*
                TODO!!!
                sets: [{
                    (entity_id?)
                    //xxx name: values.name,
                    //xxx body: values.body,
                    members: values.members,
                }],
                units: [{
                    (entity_id?)
                    --or--
                    name
                    body
                    require_ids
                }, ...]
            */
        }
        return tasks.createTopic(data)
    }
})
