store = require('../modules/store')
tasks = store.tasks
{matchesRoute, ucfirst} = require('../modules/auxiliaries')

routes = [
    {path: '/settings', task: 'openSettingsRoute'}
    {path: '/notices', task: 'listNotices'}
    {path: '/users/{id}', task: 'openProfileRoute'}
    {path: '/my_sets', task: 'listUserSets'}
    {path: '/follows', task: 'listFollows'}
    {path: '/units/{id}', task: 'openUnitRoute'}
    {path: '/sets/{id}', task: 'openSetRoute'}
    {path: '/cards/{id}', task: 'openCardRoute'}
    {path: '/{kind}s/{id}/versions', task: 'openVersionsRoute'}
    {path: '/topics/create', task: 'openCreateTopic'}
    {path: '/topics/{id}/update', task: 'openUpdateTopic'}
    {path: '/topics/{id}', task: 'openTopicRoute'}
    {path: '/sets/{id}/tree', task: 'openTreeRoute'}
    {path: '/sets/{id}/choose_unit', task: 'openChooseUnit'}
    {path: '/cards/{id}/learn', task: 'openLearnCard'}
    {path: '/topics/{id}/posts/{id}/update', task: 'openUpdatePost'}
    {path: '/search', task: 'openSearch'}
]


module.exports = store.add({
    onRoute: (path) ->
        @data.formData = {}
        @data.pageData = {}
        for route in routes
            if args = matchesRoute(path, route.path)
                return tasks[route.task].apply(null, args)

    openSettingsRoute: ->
        if not @data.currentUserID or not @data.users?[@data.currentUserID]
            tasks.getCurrentUser()

    openProfileRoute: (id) ->
        tasks.getUser(id, {
            avatar: 12 * 10
            sets: true
            follows: true
            posts: true
        })

    openUnitRoute: (id) ->
        tasks.getUnit(id)
        tasks.askFollow(id)

    openSetRoute: (id) ->
        tasks.getSet(id)
        tasks.askFollow(id)

    openCardRoute: (id) ->
        tasks.getCard(id)
        tasks.askFollow(id)

    openVersionsRoute: (kind, id) ->
        tasks["list#{ucfirst(kind)}Versions"](id)

    openCreateTopic: ->
        {kind, id} = @data.routeQuery
        tasks["get#{ucfirst(kind)}"](id)

    openUpdateTopic: (id) ->
        tasks.listPosts(id)

    openTopicRoute: (id) ->
        tasks.listPosts(id)
        tasks.askFollow(id)

    openTreeRoute: (id) ->
        tasks.getSetTree(id)

    openChooseUnit: (setID) ->
        tasks.getSetUnits(setID)

    openLearnCard: (id) ->
        tasks.getCardForLearn(id)

    openUpdatePost: (topicID, postID) ->
        tasks.listPosts(topicID)

    openSearch: ->
        if q = @data.routeQuery.q
            tasks.search({q})
})
