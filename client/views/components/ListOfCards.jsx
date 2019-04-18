import get from 'lodash.get'
import React from 'react'
import { Link } from 'react-router-dom'
import { string, shape, arrayOf } from 'prop-types'
import { convertUuidToUuid58 as to58 } from 'uuid58'
import Icon from './Icon'

const CARD_KIND_NAME = {
  CHOICE: 'Choice',
  VIDEO: 'Video',
  PAGE: 'Page',
  UNSCORED_EMBED: 'Embed',
}

const CARD_KIND_ICON = {
  CHOICE: 'choice',
  VIDEO: 'video',
  PAGE: 'page',
  UNSCORED_EMBED: 'embed',
}

const CARD_KIND_URL = {
  CHOICE: 'choice',
  VIDEO: 'video',
  PAGE: 'page',
  UNSCORED_EMBED: 'unscored-embed',
}

const cardsType = arrayOf(
  shape({
    kind: string.isRequired,
    name: string.isRequired,
  })
)

export default function ListOfCards({ cards, kind }) {
  const kCards = cards.filter(({ kind: xkind }) => xkind === kind)
  if (!kCards.length) return null
  return (
    <li>
      <h3>
        {get(CARD_KIND_NAME, kind)} <Icon i={get(CARD_KIND_ICON, kind)} s="l" />
      </h3>
      <ul>
        {kCards.map(({ name, entityId }) => (
          <li>
            <Link to={`/${get(CARD_KIND_URL, kind)}-cards/${to58(entityId)}`}>
              {name}
            </Link>
          </li>
        ))}
      </ul>
    </li>
  )
}

ListOfCards.propTypes = {
  cards: cardsType,
  kind: string.isRequired,
}

ListOfCards.defaultProps = {
  cards: [],
}
