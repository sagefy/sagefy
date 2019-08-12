import React from 'react'
import { string } from 'prop-types'

export default function Advice({ returnUrl, role }) {
  return (
    role === 'sg_anonymous' && (
      <section className="Advice">
        <p>
          <em>
            Advice: We recommend{' '}
            <a href={`/sign-up?return=${returnUrl}`}>joining</a> before you{' '}
            {returnUrl.endsWith('edit') ? 'edit' : 'create'} content,
            <br />
            so you can easily continue later!
          </em>
        </p>
      </section>
    )
  )
}

Advice.propTypes = {
  returnUrl: string.isRequired,
  role: string,
}

Advice.defaultProps = {
  role: 'sg_anonymous',
}
