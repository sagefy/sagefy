const {dispatch} = require('../modules/store')
const tasks = require('../modules/tasks')
// const request = require('../modules/request')

module.exports = tasks.add({
    resetCreate() {
        dispatch({type: 'RESET_FORM_DATA'})
        dispatch({type: 'RESET_CREATE'})
    },

    updateCreateRoute({kind, step}) {
        dispatch({type: 'UPDATE_CREATE_ROUTE', kind, step})
    },

    createSetProposal(data) {
        return tasks.createTopic(data)
    },

    addMemberToFormSet({kind, id, name, body}) {
        dispatch({
            type: 'ADD_MEMBER_TO_FORM_SET',
            kind,
            id,
            name,
            body,
        })
    }
})
