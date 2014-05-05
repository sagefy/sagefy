Backbone = require('backbone')
NotificationModel = require('models/notification')

module.exports = class NotificationsCollection extends Backbone.UsersCollection
    model: NotificationModel
