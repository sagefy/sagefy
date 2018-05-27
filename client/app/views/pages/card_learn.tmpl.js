const get = require('lodash.get')
const isNumber = require('lodash.isnumber')
const { div, a, p } = require('../../helpers/tags')
const spinner = require('../components/spinner.tmpl')
// const c = require('../../helpers/content').get
const icon = require('../components/icon.tmpl')
const { getIsLoggedIn } = require('../../selectors/base')
const goLogin = require('../../helpers/go_login')

const kindTmpl = {}
kindTmpl.video = require('./card_learn_video.tmpl')
kindTmpl.page = require('./card_learn_page.tmpl')
kindTmpl.choice = require('./card_learn_choice.tmpl')
kindTmpl.unscored_embed = require('./card_learn_unscored_embed.tmpl')

const kind = (card, mode) => {
  const fn = kindTmpl[card.kind]
  if (fn) {
    return fn(card, mode)
  }
  return null
}

module.exports = data => {
  if (getIsLoggedIn(data) === null) {
    return spinner()
  }
  if (!getIsLoggedIn(data)) {
    return goLogin()
  }
  const id = data.routeArgs[0]
  const card = get(data, `learnCards[${id}]`)
  if (!card) {
    return spinner()
  }
  const pLearned = get(data, `unitLearned[${card.unit_id}]`)

  let mode = 'next-please'
  if (card.kind === 'choice' && !isNumber(data.cardResponse.score)) {
    mode = 'answer'
  }

  let feedbackLabel = 'accent'
  if (isNumber(data.cardResponse.score)) {
    feedbackLabel = data.cardResponse.score === 1 ? 'good' : 'bad'
  }

  return [
    div(
      {
        id: 'card-learn',
        className: `page ${card.kind}-kind ${mode}`,
        key: 'WbrGhHy5aUCmBVtHnlmTdJ1x',
      },
      kind(card, mode),
      data.cardFeedback
        ? p(
            { className: `card-learner__feedback--${feedbackLabel}` },
            icon(feedbackLabel),
            ' ',
            data.cardFeedback
          )
        : null,
      p(
        a(
          {
            id,
            className: 'continue card-learner__continue',
          },
          'Continue ',
          icon('next')
        )
      )
    ),
    div({
      key: '0Xe4fksADWwm9qWOMuTl7thD',
      className: 'card-learn__progress',
      style: `width:${(pLearned || 0) * 100}%`,
    }),
  ]
}
