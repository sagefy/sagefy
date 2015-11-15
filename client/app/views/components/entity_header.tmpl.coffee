{header, span, h1, ul, li} = require('../../modules/tags')
c = require('../../modules/content').get
{ucfirst} = require('../../modules/auxiliaries')

module.exports = (kind, entity) ->
    title = ucfirst(kind)
    if kind is 'card'
        title = ucfirst(entity.kind) + ' ' + title

    return header(
        span({className: 'label--accent font-size-accent'}, title)
        h1(entity.name)
        ul(
            li("Language: #{c(entity.language)}")
            li("Tags: #{entity.tags.join(', ')}")
        )
    )
