import React from 'react'
import { number } from 'prop-types'

export default function Meter({ width }) {
  return (
    <div className="meter">
      <div style={{ width: `${width * 100}%` }} />
    </div>
  )
}

Meter.propTypes = {
  width: number.isRequired,
}
