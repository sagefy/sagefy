import React from 'react'
import { arrayOf, shape, bool } from 'prop-types'
import { Link } from 'react-router-dom'
import { convertUuidToUuid58 as to58 } from 'uuid58'
import Icon from './Icon'

export default function ChooseSubject({ subjects, active }) {
  if (!active) {
    return (
      <ul className="ChooseSubject list-style-none">
        {subjects.map(({ entityId, name, body }) => (
          <li className="collapse-margins" key={`choose-subject-${entityId}`}>
            <h3>{name}</h3>
            <p>{body}</p>
          </li>
        ))}
      </ul>
    )
  }
  return (
    <table className="ChooseSubject">
      {subjects.map(({ entityId, name, body }) => (
        <tr key={`choose-subject-${entityId}`}>
          <td className="text-align-center collapse-margins">
            <p>
              <Link to={`/next?subjectId=${to58(entityId)}`} className="button">
                <Icon i="select" />
              </Link>
            </p>
          </td>
          <td className="collapse-margins">
            <h3>
              <Link to={`/next?subjectId=${to58(entityId)}`}>{name}</Link>
            </h3>
            <p>{body}</p>
          </td>
        </tr>
      ))}
    </table>
  )
}

ChooseSubject.propTypes = {
  subjects: arrayOf(shape({})).isRequired,
  active: bool,
}

ChooseSubject.defaultProps = {
  active: true,
}
