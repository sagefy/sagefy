import React from 'react'
import { string, shape, arrayOf } from 'prop-types'
import { convertUuidToUuid58 as to58 } from 'uuid58'
import ReactMarkdown from 'react-markdown'
import Icon from './Icon'
import shorten from '../../util/shorten'

const subjectsType = arrayOf(
  shape({
    entityId: string.isRequired,
    name: string.isRequired,
    body: string.isRequired,
  })
)

export default function ListOfSubjects({ subjects, title, itemProp, icon }) {
  if (!subjects.length) return null
  return (
    <section itemProp={itemProp}>
      <h2>
        {title} <Icon i={icon} s="h2" />
      </h2>
      <ul>
        {subjects.map(({ entityId, name, body }) => (
          <li className="my-c">
            <h3>
              <a href={`/subjects/${to58(entityId)}`}>{name}</a>
            </h3>
            <ReactMarkdown
              source={shorten(body)}
              disallowedTypes={['heading']}
            />
          </li>
        ))}
      </ul>
    </section>
  )
}

ListOfSubjects.propTypes = {
  subjects: subjectsType,
  title: string.isRequired,
  icon: string.isRequired,
  itemProp: string,
}

ListOfSubjects.defaultProps = {
  subjects: [],
  itemProp: null,
}
