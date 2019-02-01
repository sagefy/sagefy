import React from 'react'
import { Link } from 'react-router-dom'
import Icon from './Icon'

export default function Footer() {
  return (
    <footer>
      <hr />
      <small>
        <ul className="list-style-inline">
          <li>
            <a
              href="https://docs.sagefy.org/"
              target="_blank"
              rel="noopener noreferrer"
            >
              <Icon i="docs" s="s" /> Docs
            </a>
          </li>
          <li>
            <a
              href="https://stories.sagefy.org/"
              target="_blank"
              rel="noopener noreferrer"
            >
              <Icon i="stories" s="s" /> Stories
            </a>
          </li>
          <li>
            <a
              href="https://sgef.cc/devupdates"
              target="_blank"
              rel="noopener noreferrer"
            >
              <Icon i="updates" s="s" /> Updates
            </a>
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
