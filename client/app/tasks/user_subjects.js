const request = require('../helpers/request')

module.exports = store => {
  const { getTasks, getState, dispatch } = store
  store.addTasks({
    listUserSubjects(userId, limit = 50, skip = 0) {
      const userID = userId || getState().currentUserID
      dispatch({ type: 'LIST_USER_SUBJECTS' })
      return request({
        method: 'GET',
        url: `/s/users/${userID}/subjects`,
        data: { limit, skip },
        rq: store.requestCookie, // SSR only
      })
        .then(response => {
          dispatch({
            type: 'ADD_USER_SUBJECTS',
            subjects: response.subjects,
            message: 'list user subjects success',
          })
        })
        .catch(errors => {
          dispatch({
            type: 'SET_ERRORS',
            message: 'list user subjects failure',
            errors,
          })
        })
    },

    addUserSubject(subjectId) {
      const userID = getState().currentUserID
      dispatch({ type: 'ADD_USER_SUBJECT', subjectId })
      return request({
        method: 'POST',
        url: `/s/users/${userID}/subjects/${subjectId}`,
        data: {},
        rq: store.requestCookie, // SSR only
      })
        .then(response => {
          dispatch({
            type: 'ADD_USER_SUBJECTS',
            subjects: [response.subject],
            message: 'add user subject success',
          })
          getTasks().route('/my_subjects')
          return response
        })
        .catch(errors => {
          dispatch({
            type: 'SET_ERRORS',
            message: 'add user sesubjectt failure',
            errors,
          })
          getTasks().route('/my_subjects')
        })
    },

    chooseSubject(subjectId) {
      const userID = getState().currentUserID
      dispatch({ type: 'CHOOSE_SUBJECT', subjectId })
      return request({
        method: 'PUT',
        url: `/s/users/${userID}/subjects/${subjectId}`,
        data: {},
        rq: store.requestCookie, // SSR only
      })
        .then(response => {
          dispatch({ type: 'CHOOSE_SUBJECT_SUCCESS', subjectId })
          getTasks().updateMenuContext({
            subject: subjectId,
            unit: false,
            card: false,
          })
          dispatch({
            type: 'SET_NEXT',
            next: response.next,
          })
          getTasks().route(`/subjects/${subjectId}/choose_unit`)
        })
        .catch(errors => {
          dispatch({
            type: 'SET_ERRORS',
            message: 'choose subject failure',
            errors,
          })
        })
    },

    removeUserSubject(subjectId) {
      const userID = getState().currentUserID
      dispatch({ type: 'REMOVE_USER_SUBJECT', subjectId })
      return request({
        method: 'DELETE',
        url: `/s/users/${userID}/subjects/${subjectId}`,
        data: {},
        rq: store.requestCookie, // SSR only
      })
        .then(() => {
          // TODO-1 remove from the state
          dispatch({ type: 'REMOVE_USER_SUBJECT_SUCCESS', subjectId })
        })
        .catch(errors => {
          dispatch({
            type: 'SET_ERRORS',
            message: 'remove user subject failure',
            errors,
          })
        })
    },
  })
}
