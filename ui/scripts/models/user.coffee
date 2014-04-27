define([
    'backbone'
    'modules/mixins'
], (Backbone, mixins) ->

    class UserModel extends Backbone.Model

        urlRoot: '/api/users/'

        fields: [
            # id
            # created
            # modified
            {
                name: 'username'
                title: 'Username'
                type: 'text'
                placeholder: 'e.g. Marissa'
                validations: {
                    required: true
                }
            }
            {
                name: 'email'
                title: 'Email'
                type: 'email'
                placeholder: 'e.g. marissa@example.com'
                description: 'We hate spam too. But we\'ll need it to get you setup.'
                validations: {
                    required: true
                    email: true
                }
            }
            {
                name: 'password'
                title: 'Password'
                type: 'password'
                description: 'Minimum 8 characters.'
                validations: {
                    required: true
                    minlength: 8
                }
            }
        ]

        validate: mixins.validateModelFromFields
        parseAjaxError: mixins.parseAjaxError

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

)
