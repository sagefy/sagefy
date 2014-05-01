define([
    'jquery'
    'views/form'
    'models/user'
], ($, FormView, UserModel) ->

    class Settings extends FormView

        title: 'Settings'
        addID: 'settings'
        fields: ['username', 'email']  # password, avatar, notifications
        description: 'All fields autosave.'
        edit: true

        beforeInitialize: ->
            @model = new UserModel({ id: 'current' })



)
