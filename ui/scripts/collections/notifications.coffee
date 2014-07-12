Backbone = require('backbone')
NotificationModel = require('../models/notification')

class NotificationsCollection extends Backbone.UsersCollection
    url: '/api/notifications/'
    model: NotificationModel

module.exports = NotificationsCollection
