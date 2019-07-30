import React from 'react'
import { string } from 'prop-types'
import Icon from './Icon'
import ExternalLink from './ExternalLink'

export default function Footer({ role }) {
  return (
    <footer>
      <hr />
      <small>
        {(role === 'sg_anonymous' && (
          <ul className="ls-i">
            <li>
              <a href="/log-in">
                <Icon i="logIn" s="s" /> Log In
              </a>
            </li>
            <li>
              <a href="/sign-up">
                <Icon i="signUp" s="s" /> Sign Up
              </a>
            </li>
          </ul>
        )) || (
          <ul className="ls-i">
            <li>
              <a href="/dashboard">
                <Icon i="dashboard" s="s" /> Dashboard
              </a>
            </li>
            <li>
              <a href="/settings">
                <Icon i="settings" s="s" /> Settings
              </a>
            </li>
            <li>
              <a href="/log-out">
                <Icon i="logOut" s="s" /> Log Out
              </a>
            </li>
            {/* TODO add notices/follows */}
          </ul>
        )}
        <ul className="ls-i">
          <li>
            <a href="/">
              <Icon i="home" s="s" /> Home
            </a>
          </li>
          <li>
            <a href="/search">
              <Icon i="search" s="s" /> Search
            </a>
          </li>
          <li>
            <ExternalLink href="https://docs.sagefy.org/">
              <Icon i="docs" s="s" /> Docs
            </ExternalLink>
          </li>
          <li>
            <ExternalLink href="https://docs.sagefy.org/stories">
              <Icon i="stories" s="s" /> Stories
            </ExternalLink>
          </li>
          <li>
            <ExternalLink href="https://sgfy.xyz/updates">
              <Icon i="updates" s="s" /> Updates
            </ExternalLink>
          </li>
        </ul>
        <ul className="ls-i">
          <li>&copy; Copyright {new Date().getFullYear()} Sagefy.</li>
          <li>
            <a href="/terms">
              <Icon i="terms" s="s" /> Privacy &amp; Terms
            </a>
          </li>
          <li>
            <a href="/contact">
              <Icon i="contact" s="s" /> Contact
            </a>
          </li>
        </ul>
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
