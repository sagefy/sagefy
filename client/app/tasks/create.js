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

    createSubjectProposal(data) {
        return tasks.createTopic(data)
    },

    createSubjectData(values) {
        dispatch({
            type: 'CREATE_SUBJECT_DATA',
            values,
        })
    },

    addMemberToCreateSubject({kind, id, name, body}) {
        dispatch({
            type: 'ADD_MEMBER_TO_CREATE_SUBJECT',
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

    removeMemberFromCreateSubject({id}) {
        dispatch({
            type: 'REMOVE_MEMBER_FROM_CREATE_SUBJECT',
            id,
        })
    },

    removeUnitFromSubject({index}) {
        dispatch({
            type: 'REMOVE_UNIT_FROM_SUBJECT',
            index,
        })
    },

    createChooseSubjectForUnits({id, name}) {
        dispatch({
            type: 'CREATE_CHOOSE_SUBJECT_FOR_UNITS',
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
        const {selectedSubject} = state.create
        const data = {
            topic: {
                name: 'Add Units to This Subject',
                entity: {
                    id: selectedSubject.id,
                    kind: 'subject',
                },
            },
            post: {
                kind: 'proposal',
                body: 'Add Units to Subject',
            },
            units: state.create.units.filter(unit => !unit.entity_id),
            subjects: [{
                entity_id: selectedSubject.id,
                // TODO 43827 other fields should populate from prev version
                members: selectedSubject.units.map(unit => ({
                    kind: 'unit',
                    id: unit.entity_id,
                    // TODO 54382 some haven't been created yet...
                }))
            }],
        }
        return tasks.createTopic(data)
    }
})
