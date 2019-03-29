import React from 'react'
import { arrayOf, shape, bool } from 'prop-types'
import { Link } from 'react-router-dom'
import { convertUuidToUuid58 as to58 } from 'uuid58'
import Icon from './Icon'

function Wark({ children, when }) {
  return (when && <mark>{children}</mark>) || children
}

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
    <table className="ChooseSubject list-style-none">
      {subjects.map(({ entityId, name, body }, i) => (
        <tr key={`choose-subject-${entityId}`} className="collapse-margins">
          <td className="vertical-align-middle text-align-center">
            <Link to={`/next?subjectId=${to58(entityId)}`}>
              <Icon i="select" s="xl" />
            </Link>
          </td>
          <td className="collapse-margins">
            <h3>
              <Wark when={i === 0 && subjects.length > 1}>
                <Link to={`/next?subjectId=${to58(entityId)}`}>{name}</Link>
              </Wark>
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
