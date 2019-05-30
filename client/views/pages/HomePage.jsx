import React from 'react'
import { Link } from 'react-router-dom'
import { string, shape, arrayOf } from 'prop-types'
import Layout from '../components/Layout'
import Icon from '../components/Icon'
import Footer from '../components/Footer'
import ExternalLink from '../components/ExternalLink'
import ChooseSubject from '../components/ChooseSubject'

export default function HomePage({ hash, role, subjects }) {
  return (
    <Layout
      hash={hash}
      page="HomePage"
      title="Learn anything, adapted for you. Free."
      description="What do you want to learn? Learn for free, always. Any subject you want. And Sagefy saves you time and effort by adapting to what you know and where you want to go."
    >
      <section className="ta-c">
        <h1>
          What do you want to learn? <Icon i="search" s="h1" />
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
            &hellip;or try something popular <Icon i="popular" s="h2" />
          </h2>
          <ChooseSubject subjects={subjects} level="goal" />
        </section>
      ) : null}

      <section>
        <div className="ta-c my-c">
          <img src="/astrolabe.svg" height="120" alt="astrolabe" />
          <h2>Sagefy</h2>
          <p>
            <em>Learn anything, adapted for you. Free.</em>
          </p>
        </div>
      </section>

      <section>
        <p>
          <Icon i="open" /> <strong>Learn anything.</strong> Anyone can view,
          share, create, and edit content. Because anyone can contribute, you
          can learn anything you want.
        </p>
        <p>
          <Icon i="adapt" /> <strong>Adapted for you.</strong> Sagefy optimizes
          based on what you already know and what your goal is. Get the most out
          of your time and effort spent.
        </p>
        <p>
          <ExternalLink href="https://youtu.be/Gi99QbiSuWs">
            <Icon i="video" /> Watch the overview video
          </ExternalLink>
          .
        </p>
      </section>

      <Footer role={role} />
    </Layout>
  )
}

HomePage.propTypes = {
  hash: string.isRequired,
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
