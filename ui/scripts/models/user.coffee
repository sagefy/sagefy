define([
    'backbone'
], (Backbone) ->

    class UserModel extends Backbone.Model

        url: '/api/users'

        # id
        # created
        # modified
        # username
        # email
        # password

        validate: (attrs, options) ->
            if not attrs.username
                return "A username is required."

            if not attrs.email
                return "An email address is required."

            if not /\S+@\S+\.\S+/.test(attrs.email)
                return "A valid email address is required."

        parse: (response) ->
            response.user

        login: (data) ->

)
