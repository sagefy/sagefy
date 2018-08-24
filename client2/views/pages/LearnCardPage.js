/*

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





const closest = require('../../helpers/closest')

module.exports = (store, broker) => {
  const { getTasks } = store
  broker.add({
    'click #card-learn.choice-kind.answer .continue'(e, el) {
      if (e) {
        e.preventDefault()
      }
      const container = closest(el, '#card-learn')
      const checked = container.querySelector('[name=choice]:checked')
      const response = checked && checked.value
      if (response) {
        getTasks().respondToCard(el.id, { response })
      } else {
        getTasks().needAnAnswer()
      }
    },

    'click #card-learn.choice-kind.next-please .continue'(e) {
      if (e) {
        e.preventDefault()
      }
      getTasks().nextState()
    },

    'click #card-learn.video-kind .continue'(e, el) {
      if (e) {
        e.preventDefault()
      }
      getTasks().respondToCard(el.id, {}, true)
    },

    'click #card-learn.page-kind .continue'(e, el) {
      if (e) {
        e.preventDefault()
      }
      getTasks().respondToCard(el.id, {}, true)
    },

    'click #card-learn.unscored_embed-kind .continue'(e, el) {
      if (e) {
        e.preventDefault()
      }
      getTasks().respondToCard(el.id, {}, true)
    },
  })
}





const { div, ul, li, input, label } = require('../../helpers/tags')
const format = require('../../helpers/format')

module.exports = (data, mode) => {
  const { body, options } = data.data
  const disabled = mode === 'next-please'

  return [
    div(format(body)),
    ul(
      { className: 'options card-learn__options' },
      options.map(option =>
        li(
          { className: disabled ? 'disabled' : '' },
          input({
            type: 'radio',
            name: 'choice',
            value: option.id,
            id: option.id,
            disabled,
            key: `${data.id}-${option.id}`,
            // The key ensures the input doesn't stay selected
            // when changing questions
          }),
          ' ',
          label(
            {
              htmlFor: option.id,
              disabled,
            },
            format(option.value)
          )
        )
      )
    ),
  ]
}





const { h1, div } = require('../../helpers/tags')
// const c = require('../../helpers/content').get
const format = require('../../helpers/format')

module.exports = data => {
  const { name } = data
  const { body } = data.data
  return div(h1(name), format(body, { highestHeading: 2 }))
}




const { iframe } = require('../../helpers/tags')

module.exports = data =>
  iframe({
    className: 'unscored_embed',
    src: data.data.url,
    width: 13 * 58,
    height: 13 * 58 * 9 / 16,
    allowfullscreen: true,
  })




const { iframe } = require('../../helpers/tags')

module.exports = data =>
  iframe({
    className: 'video',
    src:
      data.data.site === 'youtube'
        ? `https://www.youtube.com/embed/${data.data.video_id}` +
          '?autoplay=1&modestbranding=1&rel=0'
        : data.data.site === 'vimeo'
          ? `https://player.vimeo.com/video/${data.data.video_id}`
          : '',
    width: 13 * 58,
    height: 13 * 58 * 9 / 16,
    allowfullscreen: true,
  })

*/
