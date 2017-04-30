const tasks = require('../modules/tasks')
const request = require('../modules/request')
const {dispatch, getState} = require('../modules/store')

module.exports = tasks.add({
    listUserSets(limit = 50, skip = 0) {
        const userID = getState().currentUserID
        dispatch({type: 'LIST_USER_SETS'})
        return request({
            method: 'GET',
            url: `/s/users/${userID}/sets`,
            data: {limit, skip},
        })
            .then((response) => {
                dispatch({
                    type: 'ADD_USER_SETS',
                    sets: response.sets,
                    message: 'list user sets success',
                })
            })
            .catch((errors) => {
                dispatch({
                    type: 'SET_ERRORS',
                    message: 'list user sets failure',
                    errors,
                })
            })
    },

    addUserSet(setID) {
        const userID = getState().currentUserID
        dispatch({type: 'ADD_USER_SET', setID})
        return request({
            method: 'POST',
            url: `/s/users/${userID}/sets/${setID}`,
            data: {},
        })
            .then((response) => {
                dispatch({
                    type: 'ADD_USER_SETS',
                    sets: [response.set],
                    message: 'add user set success',
                })
                tasks.route('/my_sets')
            })
            .catch((errors) => {
                dispatch({
                    type: 'SET_ERRORS',
                    message: 'add user set failure',
                    errors,
                })
                tasks.route('/my_sets')
            })
    },

    chooseSet(setID) {
        const userID = getState().currentUserID
        dispatch({type: 'CHOOSE_SET', setID})
        return request({
            method: 'PUT',
            url: `/s/users/${userID}/sets/${setID}`,
            data: {},
        })
            .then((response) => {
                dispatch({type: 'CHOOSE_SET_SUCCESS', setID})
                tasks.route(`/sets/${setID}/tree`)
                tasks.updateMenuContext({
                    set: setID,
                    unit: false,
                    card: false
                })
                dispatch({
                    type: 'SET_NEXT',
                    next: response.next,
                })
            })
            .catch((errors) => {
                dispatch({
                    type: 'SET_ERRORS',
                    message: 'choose set failure',
                    errors,
                })
            })
    },

    removeUserSet(setID) {
        const userID = getState().currentUserID
        dispatch({type: 'REMOVE_USER_SET', setID})
        return request({
            method: 'DELETE',
            url: `/s/users/${userID}/sets/${setID}`,
            data: {},
        })
            .then(() => {
                // TODO-1 remove from the state
                dispatch({type: 'REMOVE_USER_SET_SUCCESS', setID})
            })
            .catch((errors) => {
                dispatch({
                    type: 'SET_ERRORS',
                    message: 'remove user set failure',
                    errors,
                })
            })
    }
})
