import React from 'react'
import { Link } from 'react-router-dom'
import { string } from 'prop-types'
import Icon from '../components/Icon'
import Footer from '../components/Footer'
import ExternalLink from '../components/ExternalLink'

export default function HomePage({ role }) {
  return (
    <div className="HomePage">
      {/* <section className="text-align-center">
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
      </section> */}

      <section>
        <blockquote>
          <h1>
            Hey friends... <Icon i="friends" s="xxl" />
          </h1>

          <p>So I&apos;m rebuilding Sagefy to let anyone</p>
          <ol>
            <li>
              <em>learn</em> without an account,
            </li>
            <li>
              <em>make</em> content without an account,
            </li>
            <li>
              and to drastically <em>simplify</em> contributing.
            </li>
          </ol>
          <p>
            Sagefy is temporarily limited. But here&apos;s some things you can
            do now:
          </p>
          <ul>
            <li>
              <ExternalLink href="https://docs.sagefy.org/mocks">
                <Icon i="view" /> <strong>View</strong> the prototype
              </ExternalLink>{' '}
              of what&apos;s coming!
            </li>
            <li>
              <Link to="/sign-up">
                <Icon i="signUp" /> <strong>Sign up</strong>
              </Link>
              , and we&apos;ll let you know as we release new stuff.
            </li>
            <li>
              <ExternalLink href="https://sgfy.xyz/devupdates">
                <Icon i="updates" /> <strong>Subscribe</strong> to biweekly
                email updates
              </ExternalLink>
              .
            </li>
          </ul>
          <p>
            <small>Last updated 2019 Mar 8</small>
          </p>
        </blockquote>
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

      {/* TODO make functional
      <section>
        <h2>
          ...or try something popular <Icon i="popular" s="xl" />
        </h2>
        <table>
          <tr>
            <td className="text-align-center collapse-margins">
              <p>
                <button type="button">
                  <Icon i="up" />
                </button>
              </p>
              <code>12</code>
            </td>
            <td className="collapse-margins">
              <h3>
                <Link to="/choose-next">
                  An Introduction to Electronic Music
                </Link>
              </h3>
              <p>
                A small taste of the basics of electronic music. Learn the
                concepts behind creating and modifying sounds in an electronic
                music system. Learn the ideas behind the tools and systems we
                use to create electronic music.
              </p>
            </td>
          </tr>
        </table>
      </section> */}

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
}

HomePage.defaultProps = {
  role: 'sg_anonymous',
}
