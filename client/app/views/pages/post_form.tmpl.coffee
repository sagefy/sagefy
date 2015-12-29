{div, h1} = require('../../modules/tags')
c = require('../../modules/content').get
form = require('../components/form.tmpl')

{mergeFieldsData} = require('../../modules/auxiliaries')
{getFields, parseData} = require('./post_form.fn')

classes = (postID, data) ->
    {postKind, entityKind, cardKind} = data
    return [
        'col-6'
        if postID then 'update' else 'create'
        if postKind then "post-#{postKind}" else ''
        if entityKind then "entity-#{entityKind}" else ''
        if cardKind then "card-#{cardKind}" else ''
    ].join(' ')

module.exports = (data) ->
    {topicID, postID, repliesToID, post, formData} = parseData(data)

    return div({className: 'spinner'}) if postID and not post

    fields = getFields({
        topicID
        postID
        repliesToID
        editKind: not postID
        postKind: data.postKind or (post and post.kind)
        entityKind: data.entityKind
        cardKind: data.cardKind
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
            className: classes(postID, data)
        }
        h1(if postID then 'Update Post' else 'Create Post')
        form(fields_)
    )
