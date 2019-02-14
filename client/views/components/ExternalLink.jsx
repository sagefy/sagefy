import React from 'react'
import { node } from 'prop-types'

export default function ExternalLink(props) {
  const { children } = props
  return (
    <a {...props} target="_blank" rel="noopener noreferrer">
      {children}
    </a>
  )
}

ExternalLink.propTypes = {
  children: node.isRequired,
}
