BaseRouter = require('./base')

class ContributorRouter extends BaseRouter
    routes: {
        'contributor(/)': 'viewDashboard'
    }

    viewDashboard: ->


module.exports = ContributorRouter
