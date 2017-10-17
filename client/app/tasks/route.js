const { dispatch, getState } = require('../modules/store')
const tasks = require('../modules/tasks')
const { matchesRoute, ucfirst } = require('../modules/auxiliaries')

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

module.exports = tasks.add({
    onRoute(path) {
        dispatch({ type: 'RESET_FORM_DATA' })
        dispatch({ type: 'RESET_ERRORS' })
        dispatch({ type: 'RESET_SEARCH' })
        for (const route of routes) {
            const args = matchesRoute(path, route.path)
            if (args) {
                return tasks[route.task].apply(null, args)
            }
        }
    },

    openSettingsRoute() {
        if (
            !getState().currentUserID ||
            !getState().users ||
            !getState().users[getState().currentUserID]
        ) {
            return tasks.getCurrentUser()
        }
    },

    openProfileRoute(id) {
        return tasks.getUserForProfile(id, { avatar: 12 * 10 })
    },

    openUnitRoute(id) {
        return Promise.all([
            tasks.getUnit(id),
            tasks.listUnitVersions(id),
            tasks.listTopics({ entity_id: id }),
            tasks.askFollow(id),
        ])
    },

    openSubjectRoute(id) {
        return Promise.all([
            tasks.getSubject(id),
            tasks.listSubjectVersions(id),
            tasks.listTopics({ entity_id: id }),
            tasks.askFollow(id),
        ])
    },

    openCardRoute(id) {
        return Promise.all([
            tasks.getCard(id),
            tasks.listCardVersions(id),
            tasks.listTopics({ entity_id: id }),
            tasks.askFollow(id),
        ])
    },

    openVersionsRoute(kind, id) {
        return tasks[`list${ucfirst(kind)}Versions`](id)
    },

    openCreateTopic() {
        const { kind, id } = getState().routeQuery
        return tasks[`get${ucfirst(kind)}`](id)
    },

    openUpdateTopic(id) {
        return tasks.listPostsForTopic(id)
    },

    openTopicRoute(id) {
        return Promise.all([tasks.listPostsForTopic(id), tasks.askFollow(id)])
    },

    openTreeRoute(id) {
        return tasks.getSubjectTree(id)
    },

    openChooseUnit(subjectId) {
        return tasks.getSubjectUnits(subjectId)
    },

    openLearnCard(id) {
        return tasks.getCardForLearn(id)
    },

    openUpdatePost(topicID /* , postID */) {
        return tasks.listPostsForTopic(topicID)
    },

    openSearch() {
        const q = getState().routeQuery.q
        if (q) {
            return tasks.search({ q })
        }
    },

    openFindSubjectForUnits() {
        return tasks.getMyRecentSubjects()
    },

    openFindUnitForCards() {
        return tasks.getMyRecentUnits()
    }
})
