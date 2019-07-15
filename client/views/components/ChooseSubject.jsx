import React from 'react'
import { arrayOf, shape, oneOf } from 'prop-types'
import { convertUuidToUuid58 as to58 } from 'uuid58'
import ReactMarkdown from 'react-markdown'
import Icon from './Icon'
import shorten from '../../util/shorten'

function Wark({ children, when }) {
  return (when && <mark>{children}</mark>) || children
}

export default function ChooseSubject({ subjects, level }) {
  return (
    <table className="ChooseSubject">
      {subjects.map(({ entityId, name, body }, i) => (
        <tr key={`choose-subject-${entityId}`}>
          <td className="va-m ta-c">
            <a href={`/next?${level}=${to58(entityId)}`}>
              <Icon i="select" s="h2" title={name} />
            </a>
          </td>
          <td className="my-c">
            <h3>
              <Wark when={i === 0 && subjects.length > 1}>
                <a href={`/next?${level}=${to58(entityId)}`}>{name}</a>
              </Wark>
            </h3>
            <ReactMarkdown
              source={shorten(body)}
              disallowedTypes={['heading']}
            />
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
