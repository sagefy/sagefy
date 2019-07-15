import get from 'lodash.get'
import React from 'react'
import { string, shape, arrayOf } from 'prop-types'
import { convertUuidToUuid58 as to58 } from 'uuid58'
import Icon from './Icon'
import CARD_KIND from '../../util/card-kind'

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
        {get(CARD_KIND, [kind, 'name'])}{' '}
        <Icon i={get(CARD_KIND, [kind, 'icon'])} s="h3" />
      </h3>
      <ul>
        {kCards.map(({ name, entityId }) => (
          <li>
            <a
              href={`/${get(CARD_KIND, [kind, 'url'])}-cards/${to58(entityId)}`}
            >
              {name}
            </a>
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
