{div, h1, h2, ul, li, iframe, i, strong, em} = require('../../modules/tags')
c = require('../../modules/content').get
spinner = require('../components/spinner.tmpl')

followButton = require('../components/follow_button.tmpl')
entityHeader = require('../components/entity_header.tmpl')
entityTopics = require('../components/entity_topics.tmpl')
entityVersions = require('../components/entity_versions.tmpl')
entityRelationships = require('../components/entity_relationships.tmpl')

assessments = ['choice', 'number', 'match', 'formula',
               'writing', 'upload', 'embed']

threeDigits = (num) ->
    return Math.round(num * 1000) / 1000

module.exports = (data) ->
    id = data.routeArgs[0]
    card = data.cards?[id]

    return spinner() unless card

    params = card.card_parameters
    assess = card.kind in assessments

    return div(
        {id: 'card'}

        followButton('card', card.entity_id, data.follows)
        entityHeader('card', card)

        div(
            {className: 'card__preview'}
            k[card.kind](card)
        )

        ul(
            li("Language: #{c(card.language)}")
            li("Tags: #{card.tags.join(', ')}")
        )

        h2('Stats')
        ul(
            li("Number of Learners: #{params.num_learners}")
            li("Guess: #{threeDigits(params.guess)}") if assess
            li("Slip: #{threeDigits(params.slip)}") if assess
            li("Transit: #{threeDigits(params.transit)} (Default)")
        )

        entityRelationships('card', card)
        entityTopics('card', card.entity_id, card.topics)
        entityVersions('card', card.entity_id, card.versions)
    )

k = {}

k.video = (card) ->
    return iframe({
        src: "https://www.youtube.com/embed/#{card.video_id}"
        width: 300
        height: 200
        allowfullscreen: true
    })

k.choice = (card) ->
    return ul(
        li('Question: ', card.body)
        li('Options: ', ul(
            li(
                i({className: if option.correct then 'fa fa-check-circle' \
                              else 'fa fa-times-circle'})
                ' '
                strong(option.value)
                ' '
                em(option.feedback)
            ) for option in card.options
        ))
        li('Order: ', card.order)
        li('Max Options to Show: ', card.max_options_to_show)
    )
