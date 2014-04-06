define([
    'jquery'
    'backbone'
    'hbs/sections/user/login'
    'models/user'
    'modules/mixins'
], ($, Backbone, template, UserModel, mixins) ->

    class LoginView extends Backbone.View

        el: $('.page')
        template: template
        events: {
            'submit form': 'submit'
        }

        initialize: ->
            if @isLoggedIn()
                Backbone.history.navigate('/dashboard')
            @model = new UserModel()
            @render()

        render: ->
            @$el.html(@template())
            @onRender()

        onRender: ->
            document.title = 'Login to Sagefy.'
            @$el.addClass('max-width-8')
                .attr('id', 'login')
            @$form = @$el.find('form')

        submit: (e) ->
            @model = UserModel.login(@formData($form))
            @model.on('login', ->
                window.location = '/dashboard'
                # Hard redirect to get the cookie
            )

        formData: mixins.formData
        isLoggedIn: mixins.isLoggedIn


)
