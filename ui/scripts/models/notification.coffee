Backbone = require('backbone')

class NotificationModel extends Backbone.Model
    urlRoot: '/api/notifications/'

    parse: (response) ->
        response.notification

module.exports = NotificationModel
