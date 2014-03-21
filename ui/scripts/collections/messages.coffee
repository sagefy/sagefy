define([
    'backbone'
    'models/message'
], (Backbone, MessageModel) ->

    class MessagesCollection extends Backbone.UsersCollection

        model: MessageModel



)
