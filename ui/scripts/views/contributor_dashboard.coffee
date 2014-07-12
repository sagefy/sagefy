PageView = require('./page')
NotificationsView = require('./notifications')
template = require('../../templates/sections/contribute/dashboard')

# This view is a layout of other components
class ContributorDashboardView extends PageView
    id: 'contributor-dashboard'
    className: 'max-width-10'
    title: 'Contributor Dashboard'
    template: template

    render: ->
        super()
        @notificationsCollection = new NotificationsCollection()
        @notificationsView = new NotificationsView({
            $region: @$('.notifications')
            collection: @notificationsCollection
        })

module.exports = ContributorDashboardView
