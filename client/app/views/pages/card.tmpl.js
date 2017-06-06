const { div, h2, ul, li } = require('../../modules/tags')
const spinner = require('../components/spinner.tmpl')
const followButton = require('../components/follow_button.tmpl')
const entityHeader = require('../components/entity_header.tmpl')
const entityTopics = require('../components/entity_topics.tmpl')
const entityVersions = require('../components/entity_versions.tmpl')
const entityRelationships = require('../components/entity_relationships.tmpl')

const assessments = ['choice', 'number', 'match', 'formula',
                     'writing', 'upload', 'embed']
const threeDigits = num => Math.round(num * 1000) / 1000

const previewCardContent = require('../components/preview_card_content.tmpl')

module.exports = (data) => {
    const id = data.routeArgs[0]
    const card = data.cards && data.cards[id]
    if (!card) { return spinner() }
    const params = card.card_parameters || {}
    const assess = card.kind in assessments
    return div(
        { id: 'card', className: 'page' },
        followButton('card', card.entity_id, data.follows),
        entityHeader('card', card),
        previewCardContent(card),
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
