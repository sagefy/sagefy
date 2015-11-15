{header, span, h1, ul, li} = require('../../modules/tags')
c = require('../../modules/content').get
{ucfirst} = require('../../modules/auxiliaries')

module.exports = (kind, entity) ->
    header(
        span({className: 'label--accent font-size-accent'}, ucfirst(kind))
        h1(entity.name)
        ul(
            li("Language: #{c(entity.language)}")
            li("Tags: #{entity.tags.join(', ')}")
        )
    )
