import React from 'react'
import { Link } from 'react-router-dom'
import { string, shape, arrayOf } from 'prop-types'
import { convertUuidToUuid58 as to58 } from 'uuid58'
import Icon from './Icon'

const subjectsType = arrayOf(
  shape({
    entityId: string.isRequired,
    name: string.isRequired,
    body: string.isRequired,
  })
)

export default function ListOfSubjects({ subjects, title, icon }) {
  if (!subjects.length) return null
  return (
    <section>
      <h2>
        {title} <Icon i={icon} s="xl" />
      </h2>
      <ul>
        {subjects.map(({ entityId, name, body }) => (
          <li>
            <strong>
              <Link to={`/subjects/${to58(entityId)}`}>{name}</Link>
            </strong>
            : {body}
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
}

ListOfSubjects.defaultProps = {
  subjects: [],
}
