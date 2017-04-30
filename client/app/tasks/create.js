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

    wantCreateSet(values) {
        dispatch({
            type: 'WANT_CREATE_SET',
            values,
        })
    },
})
