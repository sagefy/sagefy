Router = require('./framework/router')
util = require('./framework/utilities')

createPage = ->
    page = document.createElement('div')
    page.classList.add('page')
    document.body.appendChild(page)
    return page

createMenu = ->  # TODO

createStores = ->  # TODO

bindLinks = ->
    # When we click an internal link, use `navigate` instead
    # TODO update to new framework
    document.body.addEventListener('click', (e) =>
        el = util.closest(e.target, document.body, 'a')
        if not el
            return

        # Navigate to in-app URLs instead of new page
        if el.matches('[href^="/"]')
            e.preventDefault()
            @navigate(el.pathname)
        # Do nothing on empty links
        else if el.matches('[href="#"]')
            e.preventDefault()
        # Open external URLs in new windows
        else if el.matches('[href*="//"]')
            el.target = '_blank'
    )

createRouter = ->
    return new Router({
        region: createPage()
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
            ['/posts/create', require('./views/pages/post_form')]
            ['/topics/{id}', require('./views/pages/topic')]
            ['/cards/{id}', require('./views/pages/card')]
            ['/units/{id}', require('./views/pages/unit')]
            ['/sets/{id}', require('./views/pages/set')]
            ['/follows', require('./views/pages/follows')]
            ['/my_sets', require('./views/pages/my_sets')]
            ['/choose_unit', require('./views/pages/choose_unit')]
            ['/cards/{id}/learn', require('./views/pages/card_learn')]
            [/^\/?$/, require('./views/pages/index')]  # Must be 2nd to last
            [/.*/, require('./views/pages/error')]  # Must be last
        ]
    })

go = ->
    bindLinks()
    createStores()
    createRouter()
    createMenu()

modules.exports = {
    createPage: createPage
    createMenu: createMenu
    bindLinks: bindLinks
    createRouter: createRouter
    go: go
}
