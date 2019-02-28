import React from 'react'
import { Link } from 'react-router-dom'
import Icon from '../components/Icon'
// import ExternalLink from '../components/ExternalLink'

export default function ContactPage() {
  return (
    <div className="DashboardPage">
      <section>
        <h1>
          Welcome to Sagefy <Icon i="signUp" s="xxl" />
        </h1>
        <p>
          I&apos;ve reserved your user name and password! That said, there
          isn&apos;t much to do right now.
        </p>
        <p>
          <Link to="/">
            Go back <Icon i="home" /> home
          </Link>{' '}
          &bull;{' '}
          <Link to="/settings">
            Change your <Icon i="settings" /> settings
          </Link>{' '}
          &bull;{' '}
          <Link to="/log-out">
            <Icon i="logOut" /> Log Out
          </Link>
        </p>
      </section>
    </div>
  )
}
