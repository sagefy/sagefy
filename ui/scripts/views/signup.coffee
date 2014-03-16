define([
    'jquery'
    'backbone'
    'hbs/sections/user/signup'
    'parsley'
    'models/user'
    'modules/mixins'
], ($, Backbone, template, parsley, UserModel, mixins) ->

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

            @$el.find('form').parsley()

        submit: (e) ->
            e.preventDefault()
            $form = $(e.target).closest('form')
            data = @formData($form)
            @model.save(data)

        formData: mixins.formData



)
