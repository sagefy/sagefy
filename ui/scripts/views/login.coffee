define([
    'jquery'
    'backbone'
    'parsley'
    'hbs/sections/user/login'
    'models/user'
    'modules/mixins'
], ($, Backbone, parsley, template, UserModel, mixins) ->

    class LoginView extends Backbone.View

        el: $('#page')
        template: template
        events: {
            'submit form': 'submit'
        }

        initialize: ->
            @render()

        render: ->
            document.title = 'Login to Sagefy.'
            @$el.addClass('max-width-8')
                .attr('id', 'login')
                .html(@template())

        submit: (e) ->
            $form = $(e.target).closest('form')
            data = @formData($form)
            @model = UserModel.login(data)

        formData: mixins.formData



)
