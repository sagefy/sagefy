const request = require('../helpers/request')

module.exports = store => {
  const { getTasks, dispatch } = store
  return store.addTasks({
    getEntity(kind, entityId) {
      if (kind === 'card') {
        return getTasks().getCard(entityId)
      } else if (kind === 'unit') {
        return getTasks().getUnit(entityId)
      } else if (kind === 'subject') {
        return getTasks().getSubject(entityId)
      }
      return null
    },

    listEntityVersionsByTopic(id, entityVersions) {
      const total = entityVersions.length
      let count = 0
      return new Promise((resolve, reject) => {
        if (total === 0) {
          resolve()
        }
        entityVersions.forEach(ev => {
          request({
            method: 'GET',
            url: `/s/${ev.kind}s/versions/${ev.id}`,
            rq: store.requestCookie, // SSR only
          })
            .then(response => {
              const ahh = ev.kind.toUpperCase()
              dispatch({
                type: `ADD_TOPIC_POST_VERSIONS_${ahh}`,
                version: response.version,
              })
              count += 1
              if (count === total) {
                resolve()
              }
            })
            .catch(errors => {
              dispatch({
                type: 'SET_ERRORS',
                message: 'get versions for topic failure',
                errors,
              })
              reject()
            })
        })
      })
      //
    },

    listEntitiesByFollows(follows) {
      const entities = follows.map(follow => follow.entity)
      const total = entities.length
      let count = 0
      return new Promise((resolve, reject) => {
        entities.forEach(entity => {
          request({
            method: 'GET',
            url: `/s/${entity.kind}s/${entity.id}`,
            rq: store.requestCookie, // SSR only
          })
            .then(response => {
              dispatch({
                type: `ADD_${entity.kind.toUpperCase()}`,
                [entity.kind]: response[entity.kind],
              })
              count += 1
              if (count === total) {
                resolve()
              }
            })
            .catch(errors => {
              dispatch({
                type: 'SET_ERRORS',
                message: 'list entities follows failure',
                errors,
              })
              reject()
            })
        })
      })
    },
  })
}
