import React from 'react'
import { Link } from 'react-router-dom'
import Icon from '../components/Icon'

export default function HomePage() {
  return (
    <div className="HomePage">
      <section className="text-align-center">
        <h1>
          What do you want to learn? <Icon i="learn" s="xxl" />
        </h1>
        <form action="/search-subjects">
          <p>
            <input
              type="search"
              size="40"
              placeholder="example: Music"
              autoFocus
              name="q"
            />
          </p>
          <p>
            <button type="submit">
              <Icon i="search" /> Search
            </button>
          </p>
        </form>
      </section>

      {/* Change to link to go to Choose Subject page */}
      {/* <section className="text-align-right">
        <p>
          <small>
            <Link to="/log-in">➡️ Log In</Link> or
            <Link to="/sign-up">👩🏾‍💻 Sign Up</Link>
          </small>
        </p>
      </section>

      {/* <section>
        <h2>...or try something popular ✨</h2>
        <ul className="list-style-none">
          <li className="collapse-margins">
            <h3>
              <Link to="/choose-unit">🎧 An Introduction to Electronic Music</Link>
            </h3>
            {/*  This should immediately launch the learning experience!
            <p>
              A small taste of the basics of electronic music. Learn the concepts
              behind creating and modifying sounds in an electronic music system.
              Learn the ideas behind the tools and systems we use to create
              electronic music.
            </p>
          </li>
        </ul>
      </section>  */}

      <section>
        <table>
          <tr>
            <td className="text-align-right">
              <img src="/astrolabe.svg" height="120" alt="astrolabe" />
            </td>
            <td className="collapse-margins vertical-align-middle">
              <h2>Sagefy</h2>
              <p>
                <em>Learn anything, adapted to you. Free.</em>
              </p>
            </td>
          </tr>
        </table>

        <ul>
          <li>
            <Icon i="adapt" /> <strong>Adaptive Learning.</strong> Sagefy
            optimizes based on what you already know and what your goal is. Get
            the most out of your time and effort spent.
          </li>
          <li>
            <Icon i="open" /> <strong>Open-Content.</strong> Anyone can view,
            share, create, and edit content. Because anyone can contribute, you
            can learn anything you want.
          </li>
          <li>
            <Icon i="video" />{' '}
            <a
              href="https://youtu.be/gFn4Q9tx7Qs"
              target="_blank"
              rel="noopener noreferrer"
            >
              Watch the overview video
            </a>
            .
          </li>
        </ul>
      </section>

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
    </div>
  )
}
