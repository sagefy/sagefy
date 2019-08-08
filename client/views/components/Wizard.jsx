import React from 'react'
import { arrayOf, shape, string, number } from 'prop-types'
import Icon from './Icon'

function Wizard({ steps, currentIndex }) {
  return (
    <ol className="Wizard">
      {steps.map(({ name, icon }, index) => (
        <li key={`Wizard-steps-${name}`}>
          {index === currentIndex ? (
            <strong>
              {name} <Icon i={icon} />
            </strong>
          ) : (
            <span>
              {name} <Icon i={icon} />
            </span>
          )}
        </li>
      ))}
    </ol>
  )
}

Wizard.propTypes = {
  steps: arrayOf(
    shape({
      name: string.isRequired,
      icon: string.isRequired,
    })
  ).isRequired,
  currentIndex: number,
}

Wizard.defaultProps = {
  currentIndex: -1,
}
