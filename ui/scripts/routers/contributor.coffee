BaseRouter = require('./base')
PageController = require('../controllers/page')
ContributorDashboardView = require('../views/contributor_dashboard')
UserModel = require('../models/user')

class ContributorRouter extends BaseRouter
    routes: {
        'contribute(/)': 'viewDashboard'
    }

    viewDashboard: ->
        @controller = new PageController({
            view: ContributorDashboardView
        })


module.exports = ContributorRouter
