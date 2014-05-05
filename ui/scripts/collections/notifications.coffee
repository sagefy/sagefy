define([
    'backbone'
    'models/notification'
], (Backbone, NotificationModel) ->

    class NotificationsCollection extends Backbone.UsersCollection

        model: NotificationModel


)
