import React from 'react'
import { arrayOf, shape, oneOf } from 'prop-types'
import { Link } from 'react-router-dom'
import { convertUuidToUuid58 as to58 } from 'uuid58'
import ReactMarkdown from 'react-markdown'
import Icon from './Icon'

function Wark({ children, when }) {
  return (when && <mark>{children}</mark>) || children
}

export default function ChooseSubject({ subjects, level }) {
  return (
    <table className="ChooseSubject">
      {subjects.map(({ entityId, name, body }, i) => (
        <tr key={`choose-subject-${entityId}`}>
          <td className="va-m ta-c">
            <Link to={`/next?${level}=${to58(entityId)}`}>
              <Icon i="select" s="h2" title={name} />
            </Link>
          </td>
          <td className="m-yc">
            <h3>
              <Wark when={i === 0 && subjects.length > 1}>
                <Link to={`/next?${level}=${to58(entityId)}`}>{name}</Link>
              </Wark>
            </h3>
            <ReactMarkdown source={body} disallowedTypes={['heading']} />
          </td>
        </tr>
      ))}
    </table>
  )
}

ChooseSubject.propTypes = {
  subjects: arrayOf(shape({})).isRequired,
  level: oneOf(['goal', 'step']).isRequired,
}
