const { div, a, h2, ul, li, p } = require('../../modules/tags')
const timeago = require('./timeago.tmpl')
const icon = require('./icon.tmpl')

module.exports = (kind, entityID, topics) => {
    return div(
        { className: 'entity-topics' },
        h2('Topics'),
        a(
            {
                href: `/topics/create?kind=${kind}&id=${entityID}`,
            },
            icon('create'),
            ' Create a new topic'
        ),
        topics && topics.length
            ? ul(
                  topics.map(topic =>
                      li(
                          timeago(topic.created, { right: true }),
                          // TODO-2 update time ago to latest post time
                          a({ href: `/topics/${topic.id}` }, topic.name)
                          // TODO-3 number of posts
                      )
                  ),
                  li(
                      a(
                          { href: `/search?kind=topic&q=${entityID}` },
                          '... See more topics ',
                          icon('next')
                      )
                  )
              )
            : null,
        topics && topics.length ? null : p('No topics yet.')
    )
}
