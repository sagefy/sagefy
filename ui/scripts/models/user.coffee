define([
    'backbone'
    'modules/mixins'
], (Backbone, mixins) ->

    class UserModel extends Backbone.Model

        urlRoot: '/api/users/'

        fields: {
            # id
            # created
            # modified
            username: {
                required: true
            }
            email: {
                required: true
                email: true
            }
            password: {
                required: true
                minlength: 8
            }
        }

        validate: mixins.validateModelFromFields

        parse: (response) ->
            return response.user

        login: (data) ->
            $.post(@urlRoot + 'login', data)
                .done(=>
                    @trigger('login')
                )
                .fail((error) =>
                    @trigger('loginError', @parseAjaxError(error))
                )

        parseAjaxError: mixins.parseAjaxError


)
