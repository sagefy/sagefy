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
                return

            @model = new UserModel()
            @model.on('login', ->
                # Hard redirect to get the cookie
                window.location = '/dashboard'
            )
            @model.on('loginError', (error) ->
                window.alert(error.message)
            )
            @render()

        render: ->
            @$el.html(@template())
            @onRender()

        onRender: ->
            document.title = 'Login to Sagefy.'
            @$el.addClass('max-width-8')
                .attr('id', 'login')
            @$form = @$el.find('form')
            @$form.validate(@model.fields)

        submit: (e) ->
            e.preventDefault()
            @model.login(@formData(@$form))

        formData: mixins.formData
        isLoggedIn: mixins.isLoggedIn


)
