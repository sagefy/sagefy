define([
    'jquery'
    'backbone'
    'hbs/sections/user/signup'
    'models/user'
    'modules/mixins'
], ($, Backbone, template, UserModel, mixins) ->

    class Signup extends Backbone.View

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
            @model.on('sync', ->
                # Hard redirect to get the cookie
                window.location = '/dashboard'
            )
            @render()

        render: ->
            @$el.html(@template())
            @onRender()

        onRender: ->
            document.title = 'Signup for Sagefy.'
            @$el.addClass('max-width-8')
                .attr('id', 'signup')
            @$form = @$el.find('form')
            @$form.validate(@model.fields)

        submit: (e) ->
            e.preventDefault()
            @model.save(@formData(@$form))

        formData: mixins.formData
        isLoggedIn: mixins.isLoggedIn


)
