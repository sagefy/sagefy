Backbone = require('backbone')
NotificationModel = require('../models/notification')

class NotificationsCollection extends Backbone.UsersCollection
    model: NotificationModel

module.exports = NotificationsCollection
