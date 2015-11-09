{div, h1, p} = require('../../modules/tags')
c = require('../../modules/content').get
form = require('../components/form.tmpl')
postSchema = require('../../schemas/post')
topicSchema = require('../../schemas/topic')
{extend} = require('../../modules/utilities')
{mergeFieldsData} = require('../../modules/auxiliaries')

getFields = (topicID) ->
    fields = [extend({
        name: 'topic.name'
        label: 'Topic Name'
    }, topicSchema.name)]

    unless topicID
        fields.push(extend({
            name: 'post.kind'
            label: 'Post Kind'
            description: '''
                A post is a plain post.
                A proposal suggests changes.
            '''
            options: [{

            }, {
                disabled: true
            }, {
                disabled: true
            }, {
                disabled: true
            }]
            inline: true
        }, postSchema.kind), extend({
            name: 'post.body'
            label: 'Post Body'
        }, postSchema.body))

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

    # TODO return div({className: 'spinner'}) unless ...

    return div(
        {
            id: 'topic-form'
            className: (if topicID then 'update' else 'create') + ' col-8'
        }
        h1(if topicID then 'Update Topic' else 'Create Topic')
        p('Entity information...')
        form(getFields(topicID))
    )
