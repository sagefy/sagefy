import React from 'react'
import { Link } from 'react-router-dom'
import Icon from './Icon'
import ExternalLink from './ExternalLink'

export default function Footer() {
  return (
    <footer>
      <hr />
      <Link to="/">
        <img src="/astrolabe.svg" height="48" alt="astrolabe" />
      </Link>
      <small>
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
            <ExternalLink href="https://sgef.cc/devupdates">
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
        © Copyright 2019 Sagefy.
      </small>
    </footer>
  )
}
