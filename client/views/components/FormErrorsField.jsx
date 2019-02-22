import React from 'react'
import get from 'lodash.get'
import { shape, string } from 'prop-types'
import Icon from './Icon'

export default function FormErrorsField({ formErrors, field }) {
  if (!get(formErrors, field)) return null
  return (
    <ul className="FormErrors list-style-none">
      {get(formErrors, field).map(message => (
        <li>
          <mark>
            <Icon i="error" /> {message}
          </mark>
        </li>
      ))}
    </ul>
  )
}

FormErrorsField.propTypes = {
  formErrors: shape({}).isRequired,
  field: string.isRequired,
}
