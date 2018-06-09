const capitalize = require('lodash.capitalize')
const matchesRoute = require('../helpers/matches_route')
const { request, route } = require('../helpers/route_actions')

const routes = [
  { path: '/settings', task: 'openSettingsRoute' },
  { path: '/notices', task: 'listNotices' },
  { path: '/users/{id}', task: 'openProfileRoute' },
  { path: '/my_subjects', task: 'listUserSubjects' },
  { path: '/follows', task: 'listFollows' },
  { path: '/units/{id}', task: 'openUnitRoute' },
  { path: '/subjects/{id}', task: 'openSubjectRoute' },
  { path: '/cards/{id}', task: 'openCardRoute' },
  { path: '/{kind}s/{id}/versions', task: 'openVersionsRoute' },
  { path: '/topics/create', task: 'openCreateTopic' },
  { path: '/topics/{id}/update', task: 'openUpdateTopic' },
  { path: '/topics/{id}', task: 'openTopicRoute' },
  { path: '/subjects/{id}/tree', task: 'openTreeRoute' },
  { path: '/subjects/{id}/choose_unit', task: 'openChooseUnit' },
  { path: '/cards/{id}/learn', task: 'openLearnCard' },
  { path: '/topics/{id}/posts/{id}/update', task: 'openUpdatePost' },
  { path: '/search', task: 'openSearch' },
  { path: '/recommended_subjects', task: 'getRecommendedSubjects' },
  { path: '/create/unit/find', task: 'openFindSubjectForUnits' },
  { path: '/create/card/find', task: 'openFindUnitForCards' },
]

module.exports = store => {
  const { getState, dispatch, getTasks } = store
  store.addTasks({
    route(path) {
      if (path !== request()) {
        window.history.pushState({}, '', path)
        route(path)
      }
    },

    onRoute(path) {
      function finish() {
        const zroute = routes.find(xroute => matchesRoute(path, xroute.path))
        if (zroute) {
          const args = matchesRoute(path, zroute.path)
          if (args) {
            return getTasks()[zroute.task].apply(null, args)
          }
        }
        return null
      }
      dispatch({ type: 'RESET_FORM_DATA' })
      dispatch({ type: 'RESET_ERRORS' })
      dispatch({ type: 'RESET_SEARCH' })
      if (!getState().checkedSession) {
        return getTasks()
          .checkSession()
          .then(finish)
      }
      return finish()
    },

    openSettingsRoute() {
      if (
        !getState().currentUserID ||
        !getState().users ||
        !getState().users[getState().currentUserID]
      ) {
        return getTasks().getCurrentUser()
      }
      return null
    },

    openProfileRoute(id) {
      return getTasks().getUserForProfile(id, { avatar: 12 * 10 })
    },

    openUnitRoute(id) {
      return Promise.all([
        getTasks().getUnit(id),
        getTasks().listUnitVersions(id),
        getTasks().listTopics({ entity_id: id }),
        getTasks().askFollow(id),
      ])
    },

    openSubjectRoute(id) {
      return Promise.all([
        getTasks().getSubject(id),
        getTasks().listSubjectVersions(id),
        getTasks().listTopics({ entity_id: id }),
        getTasks().askFollow(id),
      ])
    },

    openCardRoute(id) {
      return Promise.all([
        getTasks().getCard(id),
        getTasks().listCardVersions(id),
        getTasks().listTopics({ entity_id: id }),
        getTasks().askFollow(id),
      ])
    },

    openVersionsRoute(kind, id) {
      return getTasks()[`list${capitalize(kind)}Versions`](id)
    },

    openCreateTopic() {
      const { kind, id } = getState().routeQuery
      return getTasks()[`get${capitalize(kind)}`](id)
    },

    openUpdateTopic(id) {
      return getTasks().listPostsForTopic(id)
    },

    openTopicRoute(id) {
      return Promise.all([
        getTasks().listPostsForTopic(id),
        getTasks().askFollow(id),
      ])
    },

    openTreeRoute(id) {
      return getTasks().getSubjectTree(id)
    },

    openChooseUnit(subjectId) {
      return getTasks().getSubjectUnits(subjectId)
    },

    openLearnCard(id) {
      return getTasks().getCardForLearn(id)
    },

    openUpdatePost(topicID /* , postID */) {
      return getTasks().listPostsForTopic(topicID)
    },

    openSearch() {
      const { q } = getState().routeQuery
      if (q) {
        return getTasks().search({ q })
      }
      return null
    },

    openFindSubjectForUnits() {
      return getTasks().getMyRecentSubjects()
    },

    openFindUnitForCards() {
      return getTasks().getMyRecentUnits()
    },
  })
}
