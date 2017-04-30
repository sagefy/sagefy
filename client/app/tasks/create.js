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

    removeMemberFromCreateSet({id}) {
        dispatch({
            type: 'REMOVE_MEMBER_FROM_CREATE_SET',
            id,
        })
    }
})
