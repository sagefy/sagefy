import React from 'react'
import { Link } from 'react-router-dom'
import { string, arrayOf, shape } from 'prop-types'
import Icon from '../components/Icon'
import Footer from '../components/Footer'
import ExternalLink from '../components/ExternalLink'
import ChooseSubject from '../components/ChooseSubject'

export default function HomePage({ role, selectPopularSubjects }) {
  return (
    <div className="HomePage">
      <section className="text-align-center">
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
        <section className="text-align-right">
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
        <section className="text-align-right">
          <p>
            <small>
              <Link to="/dashboard">
                Go to <Icon i="dashboard" /> Dashboard
              </Link>
            </small>
          </p>
        </section>
      )}

      {(selectPopularSubjects.nodes.length && (
        <section>
          <h2>
            ...or try something popular <Icon i="popular" s="xl" />
          </h2>
          <ChooseSubject subjects={selectPopularSubjects.nodes} />
        </section>
      )) ||
        null}

      <section>
        <blockquote>
          <h1>
            Hey friends... <Icon i="friends" s="xxl" />
          </h1>
          <p>
            So I&apos;m rebuilding Sagefy to (1) let anyone <em>learn</em>{' '}
            without an account, (2) <em>make</em> content without an account,
            and to (3) drastically <em>simplify</em> contributing. Sagefy is
            temporarily limited. For now:
          </p>
          <ul>
            <li>
              <Icon i="subject" /> <strong>Follow</strong> some subjects! Search
              above or add below!
            </li>
            <li>
              <ExternalLink href="https://docs.sagefy.org/mocks">
                <Icon i="view" /> <strong>View</strong> the prototype
              </ExternalLink>{' '}
              of what&apos;s coming!
            </li>
            <li>
              <ExternalLink href="https://sgfy.xyz/updates">
                <Icon i="updates" /> <strong>Subscribe</strong> to biweekly
                email updates
              </ExternalLink>
              .
            </li>
          </ul>
          <p>
            <small>Last updated 2019 Mar 27</small>
          </p>
        </blockquote>
      </section>

      <section>
        <div className="text-align-center collapse-margins">
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
  selectPopularSubjects: arrayOf(shape({})),
}

HomePage.defaultProps = {
  role: 'sg_anonymous',
  selectPopularSubjects: { nodes: [] },
}
