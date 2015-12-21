{div, h1} = require('../../modules/tags')
c = require('../../modules/content').get
form = require('../components/form.tmpl')

{mergeFieldsData} = require('../../modules/auxiliaries')
{getFields, parseData} = require('./post_form.fn')

module.exports = (data) ->
    {topicID, postID, repliesToID, post, formData} = parseData(data)

    return div({className: 'spinner'}) if postID and not post

    fields = getFields({
        topicID
        postID
        repliesToID
        editKind: not postID
        postKind: data.postKind or (post and post.kind)
    })

    if postID
        fields_ = mergeFieldsData(fields, {formData})
    else
        fields_ = fields

    fields_.push({
        id: postID
        type: 'submit'
        name: 'submit'
        label: if postID then 'Update Post' else 'Create Post'
        icon: 'plus'
    })

    return div(
        {
            id: 'post-form'
            className: (if postID then 'update' else 'create') + ' col-6'
        }
        h1(if postID then 'Update Post' else 'Create Post')
        form(fields_)
    )
