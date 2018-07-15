import React from 'react'

import Icon from '../components/Icon'

// TODO fix links for SPA routing
// TODO open external in new window
// TOOD isLoggedIn prop

export function HomePageCta() {
  return (
    <a href="/sign_up" className="home__cta-button">
      <Icon name="sign-up" />
      {" Let's Learn"}
    </a>
  )
}

export function WrappedIcon({ name }) {
  return (
    <span className="home__icon-wrap">
      <Icon name={name} />
    </span>
  )
}

export function HomePageInfo() {
  return (
    <div>
      <section>
        <hgroup>
          <h2>What is Sagefy?</h2>
          <h5>Sagefy is an open-content adaptive learning platform.</h5>
        </hgroup>
        <p>
          <strong>Adaptive Learning.</strong>
          {
            ' Sagefy optimizes based on what you already know and what your goal is. Get the most out of your time and effort spent.'
          }
        </p>
        <p>
          <strong>Open-Content.</strong>
          {
            ' Anyone can view, share, create, and edit content. Because anyone can contribute, you can learn anything you want.'
          }
        </p>
        <HomePageCta />
      </section>
      <section>
        <hgroup>
          <h2>What is Sagefy?</h2>
          <h5>Sagefy is an open-content adaptive learning platform.</h5>
        </hgroup>
        <p>
          <strong>Adaptive Learning.</strong> Sagefy optimizes based on what
          you already know and what your goal is. Get the most out of your time
          and effort spent.
        </p>
        <p>
          <strong>Open-Content.</strong> Anyone can view, share, create, and
          edit content. Because anyone can contribute, you can learn anything
          you want.
        </p>
        <HomePageCta />
      </section>
      <section>
        <h2>How do I learn with Sagefy?</h2>
        <ol className="home__ul--how">
          <li>
            <img
              src="https://i.imgur.com/2QSMPNs.png"
              alt="sign up for account"
            />{' '}
            Create an account.
          </li>
          <li>
            <img
              src="https://i.imgur.com/xKRaoff.png"
              alt="search a subject"
            />{' '}
            Find and add a subject.
          </li>
          <li>
            <img src="https://i.imgur.com/MYTGawz.png" alt="choose unit" />{' '}
            Choose your unit.
          </li>
          <li>
            <img
              src="https://i.imgur.com/yjeVPiq.png"
              alt="multiple choice card"
            />{' '}
            Learn.
          </li>
        </ol>
        <HomePageCta />
      </section>
      <section>
        <h2>Popular Subjects</h2>
        <ul className="home__ul--popular-subjects">
          {/* TODO use preview--subject__head component */}
          <li>
            <div className="preview--subject__head">
              <h3>
                <i className="icon icon-subject" />{' '}
                <a href="/subjects/UIe3mx3UTQKHDG2zLyHI5w/landing">
                  An Introduction to Electronic Music
                </a>
              </h3>
              <p>
                A small taste of the basics of electronic music. Learn the
                concepts behind creating and modifying sounds in an electronic
                music system. Learn the ideas behind the tools and systems we
                use to create electronic music.
              </p>
            </div>
          </li>
        </ul>
        <HomePageCta />
      </section>
      <section>
        <h2>Why learn with Sagefy?</h2>
        <ul className="home__ul--why">
          <li>
            <WrappedIcon name="learn" />
            <span>
              <strong>Learn</strong> any subject.
            </span>
          </li>
          <li>
            <WrappedIcon name="fast" />
            <span>
              <strong>Skip</strong> what you already know.
            </span>
          </li>
          <li>
            <WrappedIcon name="grow" />
            <span>
              <strong>Build up</strong> to where you need to be.
            </span>
          </li>
          <li>
            <WrappedIcon name="search" />
            <span>
              <strong>Choose</strong> your own path.
            </span>
          </li>
          <li>
            <WrappedIcon name="learn" />
            <span>
              Learn <strong>deeply</strong>, instead of skimming the top.
            </span>
          </li>
          <li>
            <WrappedIcon name="follow" />
            <span>
              Stay <strong>motiviated</strong> with different types of cards.
            </span>
          </li>
          <li>
            <WrappedIcon name="good" />
            <span>
              Focus on what you want to learn with{' '}
              <strong>no distractions.</strong>
            </span>
          </li>
          <li>
            <WrappedIcon name="create" />
            <span>
              Create and edit <strong>any</strong> content.
            </span>
          </li>
          <li>
            <WrappedIcon name="topic" />
            <span>
              <strong>Discuss</strong> anything as you learn.
            </span>
          </li>
        </ul>
        <HomePageCta />
      </section>
      <section>
        <h2>What does Sagefy provide?</h2>
        <iframe
          width="560"
          height="315"
          title="What is Sagefy? Video"
          src="https://www.youtube.com/embed/gFn4Q9tx7Qs"
          frameBorder="0"
          allowFullScreen="true"
        />
        <p>
          Also check out the in-detail{' '}
          <a href="https://stories.sagefy.org/why-im-building-sagefy-731eb0ceceea">
            article on Medium
          </a>.
        </p>
        <HomePageCta />
      </section>
      <section>
        <h2>Comparison</h2>
        <ul>
          <li>
            <strong>Classroom</strong>: When we adapt the content to what you
            already know, we keep the motivation going and reduce effort and
            time. Classrooms are a difficult place to get personal. Sagefy
            optimizes for what you already know, every time.
          </li>
          <li>
            <strong>Learning Management Systems</strong>: Great cost and time
            savings come from using technology. LMSs are designed to support
            the classroom model. With Sagefy, you get both the benefits of
            online learning and a highly personalized experience.
          </li>
          <li>
            <strong>Closed Adaptive Systems</strong>: Pursue your own goals.
            Closed systems means only select topics are available. An
            open-content system like Sagefy reaches a range of topics.
          </li>
          <li>
            <strong>Massive Online Courses</strong>: MOOCs reach a large range,
            but offer little adaption and only support expert-created content.
            Sagefy has no deadlines -- learn when you see fit.
          </li>
          <li>
            <strong>Flash Cards</strong>: Flash cards are great for memorizing
            content. But what about integration and application of knowledge?
            Sagefy goes deeper than flash cards.
          </li>
        </ul>
        <HomePageCta />
      </section>
    </div>
  )
}

export default function HomePage() {
  /*
    if (getIsLoggedIn(data) === null) {
    return spinner()
  }
  */
  const isLoggedIn = false
  return (
    <div id="home" className="page">
      <header>
        <img
          src="/astrolabe.svg"
          className="home__logo"
          alt="astrolabe logo"
        />
        <hgroup>
          <h1>Sagefy</h1>
          <h3>Learn anything, customized for you.</h3>
          <h6>...and always free.</h6>
        </hgroup>
        {isLoggedIn ? (
          <p>
            {'Logged in. '}
            <a href="/my_subjects">
              My Subjects <Icon name="next" />
            </a>
          </p>
        ) : (
          <p>
            <a href="/log_in">
              <Icon name="log-in" /> Log In
            </a>
            {' or '}
            <a href="/sign_up">
              <Icon name="sign-up" /> Sign Up
            </a>
          </p>
        )}
      </header>
      {!isLoggedIn && <HomePageInfo />}
      <footer>
        <ul>
          <li>© Copyright 2018 Sagefy.</li>
          <li>
            <a href="https://docs.sagefy.org/">Docs</a>
          </li>
          <li>
            <a href="https://stories.sagefy.org/">Stories (Blog)</a>
          </li>
          <li>
            <a href="https://sgef.cc/devupdates">Updates</a>
          </li>
          <li>
            <a href="https://sgef.cc/feedback">
              <Icon name="contact" /> Support
            </a>
          </li>
          <li>
            <a href="/terms">
              <Icon name="terms" /> Privacy & Terms
            </a>
          </li>
        </ul>
      </footer>
    </div>
  )
}
