define([
    'jquery'
    'backbone'
    'hbs/sections/user/signup'
    'models/user'
    'modules/mixins'
], ($, Backbone, template, UserModel, mixins) ->

    class Signup extends Backbone.View

        el: $('#page')
        template: template
        events: {
            'submit form': 'submit'
        }

        initialize: ->
            @render()
            @model = new UserModel()

        render: ->
            document.title = 'Signup for Sagefy.'
            @$el.addClass('max-width-8')
                .attr('id', 'signup')
                .html(@template())

            @$form = @$el.find('form')
            @$form.validate(@model.validations)

        submit: (e) ->
            e.preventDefault()
            @model.save(@formData(@$form))
            @model.on('sync', =>
                alert('Hello ' + @model.get('username'))
            )

        formData: mixins.formData



)
