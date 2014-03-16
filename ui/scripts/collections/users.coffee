define([
    'backbone'
    'models/user'
], (Backbone, UserModel) ->

    class UsersCollection extends Backbone.UsersCollection

        model: UserModel



)
