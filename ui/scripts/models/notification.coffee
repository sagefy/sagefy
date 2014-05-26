Backbone = require('backbone')

class NotificationModel extends Backbone.Model

    url: '/api/notifications/'

    # [fields]
    # id
    # created
    # modified

    validate: (attrs, options) ->

    parse: (response) ->
        response.notification

module.exports = NotificationModel
