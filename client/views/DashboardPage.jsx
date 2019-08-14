import React from 'react'
import { string, shape, arrayOf } from 'prop-types'
import { convertUuidToUuid58 as to58 } from 'uuid58'
import get from 'lodash.get'
import Layout from './components/Layout'
import Icon from './components/Icon'
import Footer from './components/Footer'
import ChooseSubject from './components/ChooseSubject'
import CardSubjectInfo from './components/CardSubjectInfo'
import SubjectForm from './components/SubjectForm'
import CARD_KIND from '../util/card-kind'

export default function DashboardPage({
  role,
  hash,
  name: userName,
  subjects,
  mySubjects,
  myCards,
}) {
  return (
    <Layout hash={hash} page="DashboardPage" title="Dashboard" description="-">
      <section className="my-c">
        <p>
          <em>
            Hi {userName}, welcome back! <Icon i="sagefy" />
          </em>
        </p>
        {/* TODO copy should change based on state */}
        <h1>
          What do you want to learn? <Icon i="dashboard" s="h1" />
        </h1>
      </section>

      {subjects && subjects.length ? (
        <section>
          <h2>
            Choose one of your subjects <Icon i="subject" s="h2" />
          </h2>
          <ChooseSubject subjects={subjects} level="goal" />
          <div className="my-c">
            <h3>
              &hellip;or how about something else? <Icon i="search" s="h3" />
            </h3>
            <form action="/subjects/search">
              <input
                type="search"
                size="40"
                placeholder="example: Music"
                name="q"
              />
              <button type="submit">
                <Icon i="search" /> Search
              </button>
            </form>
          </div>
        </section>
      ) : (
        <section className="ta-c">
          <h2>
            Let&apos;s get you some subjects! <Icon i="search" s="h2" />
          </h2>
          {/* TODO If the user has no subjects, then also list popular subjects here */}
          <form action="/subjects/search">
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
      )}

      {/*

<section>
  <h2>You've got some new notices 🔔</h2>
  <ul className="ls-n">
    <li>
      <p>
        Eileen voted ✅ yes on your proposal on
        <a href="/talk">Music Theory</a>.
      </p>
    </li>
    <li>
      <p>
        Or,
        <strong><a href="/notices">🔔 See all your notices</a>.</strong>
      </p>
    </li>
  </ul>
</section>

*/}

      <section>
        <h2>
          Help us build Sagefy <Icon i="build" s="h2" />
        </h2>

        {!!mySubjects.length && (
          <details>
            <summary>
              <h3 className="d-ib">
                Add some cards <Icon i="card" s="h3" />
              </h3>
            </summary>
            <ul>
              {mySubjects.map(({ entityId, name, cardCount, childCount }) => (
                <li>
                  <a href={`/cards/create?subjectId=${to58(entityId)}`}>
                    Add cards to <q>{name}</q>
                  </a>{' '}
                  <small>
                    ({cardCount} cards, {childCount} child subjects)
                  </small>
                </li>
              ))}
            </ul>
          </details>
        )}

        <details>
          <summary>
            <h3 className="d-ib">
              You can make a new subject <Icon i="subject" s="h3" />
            </h3>
          </summary>
          <SubjectForm role={role} />
        </details>

        {!!mySubjects.length && (
          <details>
            <summary>
              <h3 className="d-ib">
                Review your subjects <Icon i="subject" s="h3" />
              </h3>
            </summary>
            <ul>
              {mySubjects.map(({ entityId, name }) => (
                <li>
                  <a href={`/subjects/${to58(entityId)}`}>
                    Review <q>{name}</q>
                  </a>
                </li>
              ))}
            </ul>
          </details>
        )}

        {!!myCards.length && (
          <details>
            <summary>
              <h3 className="d-ib">
                Review your cards <Icon i="card" s="h3" />
              </h3>
            </summary>
            <ul>
              {myCards.map(({ entityId, name, kind }) => (
                <li>
                  <a
                    href={`/${get(CARD_KIND, [kind, 'url'])}-cards/${to58(
                      entityId
                    )}`}
                  >
                    Review {get(CARD_KIND, [kind, 'name']).toLowerCase()} card{' '}
                    <q>{name}</q>
                  </a>
                </li>
              ))}
            </ul>
          </details>
        )}

        <details>
          <summary>
            <h3 className="d-ib">
              &hellip;or find something else <Icon i="search" s="h3" />
            </h3>
          </summary>
          <form action="/search">
            <input
              type="search"
              size="40"
              placeholder="example: Music"
              name="q"
            />
            <button type="submit">
              <Icon i="search" /> Search
            </button>
          </form>
        </details>

        <CardSubjectInfo />
      </section>

      <Footer role={role} />
    </Layout>
  )
}

DashboardPage.propTypes = {
  hash: string.isRequired,
  role: string,
  name: string,
  subjects: arrayOf(
    shape({
      entityId: string.isRequired,
      name: string.isRequired,
      body: string.isRequired,
    })
  ),
  mySubjects: arrayOf(
    shape({
      entityId: string.isRequired,
      name: string.isRequired,
    })
  ),
  myCards: arrayOf(
    shape({
      entityId: string.isRequired,
      name: string.isRequired,
      kind: string.isRequired,
    })
  ),
}

DashboardPage.defaultProps = {
  role: 'sg_anonymous',
  name: 'friend',
  subjects: [],
  mySubjects: [],
  myCards: [],
}
