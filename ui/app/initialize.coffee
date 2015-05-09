Router = require('./modules/router')
util = require('./modules/utilities')
broker = require('./modules/broker')

CardStore = require('./stores/card')
FollowStore = require('./stores/follow')
NoticeStore = require('./stores/notice')
PostStore = require('./stores/post')
SearchStore = require('./stores/search')
SetStore = require('./stores/set')
TopicStore = require('./stores/topic')
UnitStore = require('./stores/unit')
UserStore = require('./stores/user')

logAllEvents = ->
    broker.on('all', (args...) -> console.log(args...))

createStores = ->
    return {
        card: new CardStore()
        follow: new FollowStore()
        notice: new NoticeStore()
        post: new PostStore()
        search: new SearchStore()
        set: new SetStore()
        topic: new TopicStore()
        unit: new UnitStore()
        user: new UserStore()
    }

createPage = ->
    page = document.createElement('div')
    page.classList.add('page')
    document.body.appendChild(page)
    return page

createRouter = (page) ->
    return new Router({
        region: page
        routes: [
            ['/sign_up', require('./views/pages/sign_up')]
            ['/log_in', require('./views/pages/log_in')]
            ['/log_out', require('./views/pages/log_out')]
            ['/password', require('./views/pages/password')]
            ['/styleguide', require('./views/pages/styleguide')]
            ['/terms', require('./views/pages/terms')]
            ['/contact', require('./views/pages/contact')]
            ['/settings', require('./views/pages/settings')]
            ['/notices', require('./views/pages/notices')]
            ['/search', require('./views/pages/search')]
            [
                /^\/topics\/(create|[\d\w]+\/update)$/
                require('./views/pages/topic_form')
            ]  # Must be before `topic`
            [
                /^\/posts\/(create|[\d\w]+\/update)$/
                require('./views/pages/post_form')
            ]
            ['/topics/{id}', require('./views/pages/topic')]
            ['/cards/{id}', require('./views/pages/card')]
            ['/units/{id}', require('./views/pages/unit')]
            ['/sets/{id}', require('./views/pages/set')]
            ['/follows', require('./views/pages/follows')]
            ['/my_sets', require('./views/pages/my_sets')]
            ['/choose_unit', require('./views/pages/choose_unit')]
            ['/cards/{id}/learn', require('./views/pages/card_learn')]
            [/^\/?$/, require('./views/pages/home')]  # Must be 2nd to last
            [/.*/, require('./views/pages/error')]  # Must be last
        ]
    })

createMenu = ->  # TODO

go = ->
    logAllEvents()
    createStores()
    router = createRouter(createPage())
    router.activate()
    router.bindLinks()
    createMenu()
    return true

module.exports = {
    logAllEvents: logAllEvents
    createStores: createStores
    createPage: createPage
    createRouter: createRouter
    createMenu: createMenu
    go: go
}
