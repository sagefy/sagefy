FormAdapter = require('./form')
FormLayoutView = require('../views/layouts/form')
FormView = require('../views/components/form')
TopicModel = require('../models/topic')
PostModel = require('../models/post')
util = require('../framework/utilities')

class TopicFormAdapter extends FormAdapter

    title: ->
        return 'Update a Topic' if @getTopicID()
        return 'Create a New Topic'

    render: ->
        return if @requireLogIn()
        super
        @model = new TopicModel()
        @postModel = new PostModel()
        @view = new FormLayoutView({
            id: 'topic-form'
            className: 'col-6'
            region: @page
        })
        @view.render({
            title: if @getTopicID() \
                   then 'Update a Topic' \
                   else 'Create a New Topic'
        })
        @form = new FormView({
            schema: @getSchema()
            region: @view.form
        })
        @form.render()
        @bindEvents()

    getTopicID: ->
        path = window.location.pathname
        match = path.match(/^\/topics\/([\d\w]+)\/update$/)
        return match[1] if match
        return null

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
            label: if @getTopicID() \
                   then 'Update Topic' \
                   else 'Create Topic'
            icon: 'plus'
        }])

        return schema

module.exports = TopicFormAdapter
