Backbone = require('backbone')
BaseRouter = require('./base')
$ = require('jquery')

PageController = require('../controllers/page')

UserModel = require('../models/user')

MenuGlobalView = require('../views/menu--global')
StyleguideView = require('../views/styleguide')
LoginView = require('../views/login')
LogoutView = require('../views/logout')
TermsView = require('../views/terms')
TermsView = require('../views/terms')
ContactView = require('../views/contact')
SettingsView = require('../views/settings')
IndexView = require('../views/index')
SignupView = require('../views/signup')
CreatePasswordView = require('../views/create_password')
ErrorView = require('../views/error')

class PrimaryRouter extends BaseRouter
    routes: {
        'styleguide(/)': 'viewStyleguide'
        'login(/)': 'viewLogin'
        'logout(/)': 'viewLogout'
        'signup(/)': 'viewSignup'
        'terms(/)': 'viewTerms'
        'contact(/)': 'viewContact'
        'settings(/)': 'viewSettings'
        'create_password(/)': 'createPassword'
        '(/)': 'viewIndex'
        '*_': 'viewError'
    }

    initialize: ->
        @menuGlobalView = new MenuGlobalView()

        # Create the page container
        $('body').prepend('<div class="page"></div>')

        # When we click an internal link, use Navigate instead
        $('body').on('click', 'a[href^="/"]', (e) ->
            e.preventDefault()
            href = $(e.currentTarget).closest('a').attr('href')
            Backbone.history.navigate(href, {trigger: true})
        )

    viewError: ->
        @controller = new PageController({view: ErrorView})

    viewIndex: ->
        @controller = new PageController({view: IndexView})

    viewLogin: ->
        @controller = new PageController({
            view: LoginView
            model: UserModel
        })

    viewLogout: ->
        @controller = new PageController({
            view: LogoutView
            model: UserModel
            modelOptions: {id: 'current'}
        })

    viewSignup: ->
        @controller = new PageController({
            view: SignupView
            model: UserModel
        })

    viewTerms: ->
        @controller = new PageController({view: TermsView})

    viewContact: ->
        @controller = new PageController({view: ContactView})

    viewStyleguide: ->
        @controller = new PageController({view: StyleguideView})

    viewSettings: ->
        @controller = new PageController({
            view: SettingsView
            model: UserModel
            modelOptions: {id: 'current'}
        })

    createPassword: ->
        @controller = new PageController({
            view: CreatePasswordView
            model: UserModel
        })


module.exports = PrimaryRouter
