FormAdapter = require('./form')
FormLayoutView = require('../views/layouts/form')
FormView = require('../views/components/form')
TopicModel = require('../models/topic')
PostModel = require('../models/post')

class CreateTopicAdapter extends FormAdapter
    url: '/topic/create'
    title: 'Create a New Topic'

    render: ->
        return if @requireLogIn()
        super
        @model = new TopicModel()
        @postModel = new PostModel()
        @view = new FormLayoutView({
            id: 'create-topic'
            className: 'col-6'
            region: @page
        })
        @view.render({
            title: 'Create a New Topic'
        })
        @form = new FormView({
            schema: @getSchema()
            region: @view.form
        })
        @postForm = new FormView({
            schema: @getPostSchema()
            region: null
        })
        @form.render()
        @bindEvents()

    bindEvents: ->
        super

    remove: ->
        @postForm.remove()
        @postModel.remove()
        super

    getSchema: ->
        return @addModelSchema([{
            name: 'name'
            label: 'Topic Name'
            size: 40
        }])

    getPostSchema: ->
        return [ {
            name: 'submit'
            label: 'Create Topic'
            type: 'submit'
            icon: 'check'
        }]

module.exports = CreateTopicAdapter
