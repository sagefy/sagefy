const {div, h2, ul, li, iframe, strong, em} =
    require('../../modules/tags')
const c = require('../../modules/content').get
const spinner = require('../components/spinner.tmpl')
const icon = require('../components/icon.tmpl')
const followButton = require('../components/follow_button.tmpl')
const entityHeader = require('../components/entity_header.tmpl')
const entityTopics = require('../components/entity_topics.tmpl')
const entityVersions = require('../components/entity_versions.tmpl')
const entityRelationships = require('../components/entity_relationships.tmpl')

const assessments = ['choice', 'number', 'match', 'formula',
                     'writing', 'upload', 'embed']
const threeDigits = (num) => Math.round(num * 1000) / 1000

module.exports = (data) => {
    const id = data.routeArgs[0]
    const card = data.cards && data.cards[id]
    if(!card) { return spinner() }
    const params = card.card_parameters || {}
    const assess = card.kind in assessments
    return div(
        {id: 'card'},
        followButton('card', card.entity_id, data.follows),
        entityHeader('card', card),
        div(
            {className: 'card__preview'},
            k[card.kind](card)
        ),
        ul(
            li(`Language: ${c(card.language)}`),
            li(`Tags: ${card.tags.join(', ')}`)
        ),
        h2('Stats'),
        ul(
            li(`Number of Learners: ${params.num_learners}`),
            assess ? li(`Guess: ${threeDigits(params.guess)}`) : null,
            assess ? li(`Slip: ${threeDigits(params.slip)}`) : null,
            li(`Transit: ${threeDigits(params.transit)} (Default)`)
        ),
        entityRelationships('card', card),
        entityTopics('card', card.entity_id, card.topics),
        entityVersions('card', card.entity_id, card.versions)
    )
}

const k = {}

k.video = (card) =>
    iframe({
        src: `https://www.youtube.com/embed/${card.video_id}`,
        width: 300,
        height: 200,
        allowfullscreen: true,
    })

k.choice = (card) =>
    ul(
        li('Question: ', card.body),
        li('Options: ', ul(
            card.options.map(option => li(
                icon(option.correct ? 'good' : 'bad'),
                ' ',
                strong(option.value),
                ' ',
                em(option.feedback)
            ))
        )),
        li('Order: ', card.order),
        li('Max Options to Show: ', card.max_options_to_show)
    )
