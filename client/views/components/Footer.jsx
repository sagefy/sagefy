import React from 'react'
import { Link } from 'react-router-dom'
import { string } from 'prop-types'
import Icon from './Icon'
import ExternalLink from './ExternalLink'

export default function Footer({ role }) {
  return (
    <footer>
      <hr />
      <Link to="/">
        <img src="/astrolabe.svg" height="48" alt="astrolabe" />
      </Link>
      <small>
        {role !== 'sg_anonymous' && (
          <ul className="list-style-inline">
            <li>
              <Link to="/dashboard">
                <Icon i="dashboard" s="s" /> Dashboard
              </Link>
            </li>
            <li>
              <Link to="/settings">
                <Icon i="settings" s="s" /> Settings
              </Link>
            </li>
            <li>
              <Link to="/log-out">
                <Icon i="logOut" s="s" /> Log Out
              </Link>
            </li>
            {/* TODO add notices/follows */}
          </ul>
        )}
        <ul className="list-style-inline">
          <li>
            <ExternalLink href="https://docs.sagefy.org/">
              <Icon i="docs" s="s" /> Docs
            </ExternalLink>
          </li>
          <li>
            <ExternalLink href="https://stories.sagefy.org/">
              <Icon i="stories" s="s" /> Stories
            </ExternalLink>
          </li>
          <li>
            <ExternalLink href="https://sgfy.xyz/devupdates">
              <Icon i="updates" s="s" /> Updates
            </ExternalLink>
          </li>
          <li>
            <Link to="/contact">
              <Icon i="contact" s="s" /> Contact
            </Link>
          </li>
          <li>
            <Link to="/terms">
              <Icon i="terms" s="s" /> Privacy &amp; Terms
            </Link>
          </li>
        </ul>
        © Copyright {new Date().getFullYear()} Sagefy.
      </small>
    </footer>
  )
}

Footer.propTypes = {
  role: string,
}

Footer.defaultProps = {
  role: 'sg_anonymous',
}
