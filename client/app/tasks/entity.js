// const {dispatch} = require('../modules/store')
const tasks = require('../modules/tasks')
// const request = require('../modules/request')

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
        // TODO-0
        const versionsByKind = {
            card: [],
            unit: [],
            subject: [],
        }
        entityVersions.forEach((entityVersion) => {
            versionsByKind[entityVersion.kind].push(entityVersion.id)
        })

        // /s/cards/versions/{version_id}
    }
})
