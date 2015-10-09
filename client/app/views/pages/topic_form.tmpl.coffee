{div, h1} = require('../../modules/tags')
c = require('../../modules/content').get
form = require('../components/form.tmpl')
postSchema = require('../../schemas/post')
topicSchema = require('../../schemas/topic')
{extend} = require('../../modules/utilities')
{mergeFieldsData} = require('../../modules/auxiliaries')

getFields = (topicID) ->
    fields = [{
        name: 'name'
        label: 'Topic Name'
    }]  # topic schema

    unless topicID
        fields.push({
            name: 'post.kind'
            label: 'Post Kind'
        }, {
            name: 'post.body'
            label: 'Post Body'
        })  # post schema

    fields.push({
        type: 'submit'
        name: 'submit'
        label: if topicID then 'Update Topic' else 'Create Topic'
        icon: 'plus'
    })

    return fields

getTopicID = (data) ->
    match = data.route.match(/^\/topics\/([\d\w]+)\/update$/)
    return match[1] if match
    return null

module.exports = (data) ->
    topicID = getTopicID(data)

    return div(
        {
            id: 'topic-form'
            className: (if topicID then 'update' else 'create') + ' col-10'
        }
        h1(if topicID then 'Update Topic' else 'Create Topic')
        form(getFields(topicID))
    )
