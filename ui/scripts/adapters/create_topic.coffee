FormAdapter = require('./form')
FormLayoutView = require('../views/layouts/form')
FormView = require('../views/components/form')
TopicModel = require('../models/topic')
PostModel = require('../models/post')
util = require('../framework/utilities')

class CreateTopicAdapter extends FormAdapter
    url: '/topics/create'
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
        @form.render()
        @bindEvents()

    bindEvents: ->
        super

    remove: ->
        @postModel.remove()
        super

    getSchema: ->
        schema = [util.extend({
            name: 'topic__name'
            label: 'Topic Name'
            size: 40
        }, TopicModel::schema.name), util.extend({
            name: 'post__kind'
            label: 'First Post Kind'
        }, PostModel::schema.kind), util.extend({
            name: 'post__body'
            label: 'First Post Body'
            cols: 40
            rows: 4
        }, PostModel::schema.body)]

        schema = schema.concat([{
            type: 'submit'
            name: 'create-topic'
            label: 'Create Topic'
            icon: 'plus'
        }])

        return schema

module.exports = CreateTopicAdapter
