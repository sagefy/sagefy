import React from 'react'
import { Link } from 'react-router-dom'
import { string } from 'prop-types'
import Icon from '../components/Icon'

export default function CreateCardPage({ role }) {
  return (
    <div className="CreateCardPage">
      <section>
        <h1>
          &hellip; <Icon i="card" s="xxl" />
        </h1>
        <p>
          Sorry, Sagefy is temporarily limited. There are no cards yet in that
          subject. But soon you&apos;ll be able to make cards here!
        </p>
      </section>
      <section>
        <p className="ta-r">
          <small>
            Let&apos;s go{' '}
            {role === 'sg_anonymous' ? (
              <Link to="/">
                <Icon i="home" /> Home
              </Link>
            ) : (
              <Link to="/dashboard">
                to the <Icon i="dashboard" /> Dashboard
              </Link>
            )}
            .
          </small>
        </p>
      </section>
    </div>
  )
}

CreateCardPage.propTypes = {
  role: string,
}

CreateCardPage.defaultProps = {
  role: 'sg_anonymous',
}
