import React from 'react'
import { Link } from 'react-router-dom'
import { string, shape, arrayOf } from 'prop-types'
import Icon from '../components/Icon'
import Footer from '../components/Footer'
import ExternalLink from '../components/ExternalLink'
import ChooseSubject from '../components/ChooseSubject'

export default function HomePage({ role, subjects }) {
  return (
    <div className="HomePage">
      <section className="ta-c">
        <h1>
          What do you want to learn? <Icon i="search" s="xxl" />
        </h1>
        <form action="/search-subjects">
          <p>
            <input
              type="search"
              size="40"
              placeholder="example: Music"
              autoFocus
              name="q"
              aria-label="Search"
            />
          </p>
          <p>
            <button type="submit">
              <Icon i="search" /> Search
            </button>
          </p>
        </form>
      </section>

      {role === 'sg_anonymous' ? (
        <section className="ta-r">
          <p>
            <small>
              <Link to="/log-in">
                <Icon i="logIn" /> Log In
              </Link>{' '}
              or{' '}
              <Link to="/sign-up">
                <Icon i="signUp" /> Sign Up
              </Link>
            </small>
          </p>
        </section>
      ) : (
        <section className="ta-r">
          <p>
            <small>
              <Link to="/dashboard">
                Go to <Icon i="dashboard" /> Dashboard
              </Link>
            </small>
          </p>
        </section>
      )}

      {subjects && subjects.length ? (
        <section>
          <h2>
            &hellip;or try something popular <Icon i="popular" s="xl" />
          </h2>
          <ChooseSubject subjects={subjects} level="goal" />
        </section>
      ) : null}

      <section>
        <blockquote>
          <h1>
            Hey friends&hellip; <Icon i="friends" s="xxl" />
          </h1>
          <p>
            I&apos;m rebuilding Sagefy, and the rebuild is in progress. Sagefy
            is temporarily limited. While the core learning experience is now
            available, some features are not.{' '}
            <ExternalLink href="https://docs.sagefy.org/mocks">
              <strong>View</strong> the prototype
            </ExternalLink>{' '}
            of what&apos;s coming!
          </p>
          <p>
            <small>Last updated 2019 Apr 8</small>
          </p>
        </blockquote>
      </section>

      <section>
        <div className="ta-c m-yc">
          <img src="/astrolabe.svg" height="120" alt="astrolabe" />
          <h2>Sagefy</h2>
          <p>
            <em>Learn anything, adapted for you. Free.</em>
          </p>
        </div>
      </section>

      <section>
        <ul>
          <li>
            <Icon i="adapt" /> <strong>Adaptive Learning.</strong> Sagefy
            optimizes based on what you already know and what your goal is. Get
            the most out of your time and effort spent.
          </li>
          <li>
            <Icon i="open" /> <strong>Open Content.</strong> Anyone can view,
            share, create, and edit content. Because anyone can contribute, you
            can learn anything you want.
          </li>
          <li>
            <ExternalLink href="https://youtu.be/gFn4Q9tx7Qs">
              <Icon i="video" /> Watch the overview video
            </ExternalLink>
            .
          </li>
        </ul>
      </section>

      <Footer role={role} />
    </div>
  )
}

HomePage.propTypes = {
  role: string,
  subjects: arrayOf(
    shape({
      entityId: string.isRequired,
      name: string.isRequired,
      body: string.isRequired,
    })
  ),
}

HomePage.defaultProps = {
  role: 'sg_anonymous',
  subjects: [],
}
