import React from 'react'
import { shape } from 'prop-types'
import Icon from './Icon'

export default function FormErrorsTop({ formErrors }) {
  if (!Object.keys(formErrors).length) return null
  return (
    <div className="FormErrorsTop">
      <p>
        <mark>
          <Icon i="error" /> I couldn&apos;t do that...
        </mark>
      </p>
    </div>
  )
}

FormErrorsTop.propTypes = {
  formErrors: shape({}).isRequired,
}
