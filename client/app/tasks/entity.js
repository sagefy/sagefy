const { dispatch } = require('../modules/store')
const tasks = require('../modules/tasks')
const request = require('../modules/request')

module.exports = tasks.add({
    getEntity(kind, entityId) {
        if (kind === 'card') {
            return tasks.getCard(entityId)
        } else if (kind === 'unit') {
            return tasks.getUnit(entityId)
        } else if (kind === 'subject') {
            return tasks.getSubject(entityId)
        }
    },

    listEntityVersionsByTopic(id, entityVersions) {
        const total = entityVersions.length
        let count = 0
        return new Promise((resolve, reject) => {
            entityVersions.forEach((ev) => {
                request({
                    method: 'GET',
                    url: `/s/${ev.kind}s/versions/${ev.id}`,
                })
                .then((response) => {
                    const ahh = ev.kind.toUpperCase()
                    dispatch({
                        type: `ADD_TOPIC_POST_VERSIONS_${ahh}`,
                        version: response.version,
                    })
                    count++
                    if(count === total) { resolve() }
                })
                .catch((errors) => {
                    dispatch({
                        type: 'SET_ERRORS',
                        message: 'create new unit version failure',
                        errors,
                    })
                    reject()
                })
            })
        })
        //
    },
})
