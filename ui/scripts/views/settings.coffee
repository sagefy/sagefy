define([
    'jquery'
    'views/form'
    'models/user'
    'modules/mixins'
], ($, FormView, UserModel, mixins) ->

    class Settings extends FormView

        title: 'Settings'
        addID: 'settings'
        fields: ['username', 'email']  # password, avatar, notifications
        description: 'All fields autosave.'
        edit: true

        beforeInitialize: ->
            @model = new UserModel({ id: 'current' })

        onRender: ->
            @updatePageWidth(6)

        updatePageWidth: mixins.updatePageWidth


)
