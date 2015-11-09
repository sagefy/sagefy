{div, h1} = require('../../modules/tags')
c = require('../../modules/content').get
post = require('../components/post.tmpl')

module.exports = (data) ->
    return div({className: 'spinner'}) unless data.posts

    return div(
        {id: 'topic', className: 'col-10'}
        h1('Topic')
        # TODO Include a link to the entity
        post(p) for p in data.posts
        # TODO Include a button to add a new post
    )
