import React from 'react'
import { string } from 'prop-types'
import Layout from './components/Layout'
import Icon from './components/Icon'
import ExternalLink from './components/ExternalLink'

export default function AboutPage({ hash }) {
  return (
    <Layout
      hash={hash}
      page="AboutPage"
      title="About"
      description="What is Sagefy? Learn about Sagefy, where you can learn anything adapted for you. Our adaptive learning platform is free for everyone."
    >
      <header className="my-c">
        <a href="/">
          Go back <Icon i="home" /> home
        </a>
        <h1>
          What is Sagefy <Icon i="about" s="h1" />
        </h1>
      </header>
      <section>
        <p>
          <strong>Learn anything, adapted for you. Free.</strong>
        </p>
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
          First time here? Learn what Sagefy is by using it!{' '}
          <a href="/next?goal=W9UmrCsnrmgPvwp8mQRuoc" rel="nofollow">
            This 3-5 minute subject
          </a>{' '}
          will introduce you to Sagefy. You will learn what Sagefy is, how it
          works, and how to learn and contribute.
        </p>
      </section>
      <section>
        <h2>The 8 Ideas</h2>
        <p>Sagefy follows 8 learning ideas, backed by educational science:</p>
        <ol>
          <li>
            <strong>Do One Thing at a Time</strong>
          </li>
          <li>
            <strong>Set &amp; Adhere to Goals</strong>
          </li>
          <li>
            <strong>Adapt to Prior Knowledge</strong>
          </li>
          <li>
            <strong>Build the Graph</strong>
          </li>
          <li>
            <strong>Empower Choice</strong>
          </li>
          <li>
            <strong>Dive Deep</strong>
          </li>
          <li>
            <strong>Make It Real</strong>
          </li>
          <li>
            <strong>Learn Together</strong>
          </li>
        </ol>
        <p>
          For a full explanation of these ideas and sources, read{' '}
          <ExternalLink href="https://heiskr.com/stories/eight-big-ideas-of-learning">
            Eight big ideas of learning
          </ExternalLink>
          .
        </p>
      </section>
      <section>
        <h2>Cards and Subjects</h2>
        <p>
          <em>
            There are two types of entities in Sagefy: cards and subjects.
          </em>
        </p>
        <ul>
          <li>
            <p>
              A <strong>card</strong> is a single learning activity.
            </p>
            <blockquote>
              <p>Examples: a 3-minute video or a multiple choice question.</p>
            </blockquote>
          </li>
          <li>
            <p>
              A <strong>subject</strong> is a collection of cards and other
              subjects.
            </p>
            <blockquote>
              <p>
                Like a course, but at any scale. Such as “Measures of Central
                Tendency”, “Intro to Statistics”, or even a complete statistics
                program.
              </p>
            </blockquote>
          </li>
        </ul>
        <p>
          For further information on cards and subjects, read our{' '}
          <ExternalLink href="https://docs.sagefy.org/cards-subjects">
            docs article
          </ExternalLink>
          .
        </p>
      </section>
      <section>
        <h2>Even more&hellip;</h2>
        <p>Read some blog posts about Sagefy&apos;s development.</p>
        <ul className="ls-n">
          <li className="my-c">
            <h2>
              <ExternalLink href="https://heiskr.com/stories/why-i-m-building-sagefy">
                Why I’m building&nbsp;Sagefy
              </ExternalLink>
            </h2>
            <p>
              <em>
                I would like to share with you some things about a project I’ve
                been working on since early 2013.
              </em>
            </p>
            <p>
              <small>
                <time dateTime="2016-09-14">2016 Sep 14</time>
              </small>
            </p>
          </li>

          <li className="my-c">
            <h2>
              <ExternalLink href="https://heiskr.com/stories/a-new-sagefy">
                A New Sagefy
              </ExternalLink>
            </h2>
            <p>
              <em>
                What Sagefy is, where it was, and why and how I changed Sagefy.
              </em>
            </p>
            <p>
              <small>
                <time dateTime="2019-07-31">2019 Jul 31</time>
              </small>
            </p>
          </li>

          <li className="my-c">
            <h2>
              <ExternalLink href="https://heiskr.com/stories/eight-big-ideas-of-learning">
                Eight big ideas of learning
              </ExternalLink>
            </h2>
            <p>
              <em>Research-backed strategies for better learning.</em>
            </p>
            <p>
              <small>
                <time dateTime="2018-07-09">2018 Jul 09</time>
              </small>
            </p>
          </li>

          <li className="my-c">
            <h2>
              <ExternalLink href="https://heiskr.com/stories/adaptive-learning">
                How to build an adaptive learning system
              </ExternalLink>
            </h2>
            <p>
              <em>The four elements of adaptive learning systems.</em>
            </p>
            <p>
              <small>
                <time dateTime="2019-08-20">2019 Aug 20</time>
              </small>
            </p>
          </li>

          <li className="my-c">
            <h2>
              <ExternalLink href="https://heiskr.com/stories/the-mathematics-of-sagefy">
                The mathematics of Sagefy
              </ExternalLink>
            </h2>
            <p>
              <em>How Sagefy adapts to you, and where it can go.</em>
            </p>
            <p>
              <small>
                <time dateTime="2017-04-06">2017 Apr 06</time>
              </small>
            </p>
          </li>
          <li className="my-c">
            <h2>
              <ExternalLink href="https://heiskr.com/stories/choosing-an-open-source-license">
                Choosing an open-source license
              </ExternalLink>
            </h2>
            <p>
              <em>How I chose the Apache 2 license for Sagefy.</em>
            </p>
            <p>
              <small>
                <time dateTime="2016-10-16">2016 Oct 16</time>
              </small>
            </p>
          </li>
        </ul>
      </section>
    </Layout>
  )
}

AboutPage.propTypes = { hash: string.isRequired }
