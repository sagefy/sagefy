import React from 'react'
import { string, shape, arrayOf, number } from 'prop-types'
import ReactMarkdown from 'react-markdown'
import { convertUuidToUuid58 as to58 } from 'uuid58'
import Layout from '../components/Layout'
import Icon from '../components/Icon'
import Footer from '../components/Footer'
import ListOfSubjects from '../components/ListOfSubjects'
import ListOfCards from '../components/ListOfCards'
import shorten from '../../util/shorten'

const subjectsType = arrayOf(
  shape({
    entityId: string.isRequired,
    name: string.isRequired,
    body: string.isRequired,
  })
)
const cardsType = arrayOf(
  shape({
    kind: string.isRequired,
    name: string.isRequired,
  })
)

export default function SubjectPage({
  hash,
  role,
  subject: {
    entityId: subjectEntityId,
    name: subjectName,
    body: subjectBody,
    details: subjectDetails,
    childSubjects,
    beforeSubjects,
    afterSubjects,
    parentSubjects,
    cardCount,
    cards,
    image,
  },
}) {
  return (
    <Layout
      hash={hash}
      page="SubjectPage"
      title={`Learn about ${subjectName}`}
      description={`Learn about ${subjectName}, adapted and optimized for you. Learn for free, always. ${shorten(
        subjectBody
      )}`}
      image={image}
    >
      <div itemScope itemType="https://schema.org/Course">
        <header>
          <div className="my-c">
            <p>
              Subject <Icon i="subject" />
            </p>
            <h1 itemProp="name">{subjectName}</h1>
          </div>
          {image && (
            <img
              src={image}
              style={{ maxHeight: 16 * 10, width: '100%', objectFit: 'cover' }}
              itemProp="image"
              alt="flickr"
            />
          )}
          <div itemProp="description">
            <ReactMarkdown source={subjectBody} disallowedTypes={['heading']} />
          </div>
          <form method="GET" action="/next">
            <input type="hidden" name="goal" value={to58(subjectEntityId)} />
            <button type="submit">
              <Icon i="select" /> Let&apos;s learn now
            </button>
          </form>
          <small>
            <ul className="ls-i ta-r">
              {/* <li><a href="/mocks/follows">👂🏿 Follow</a></li> */}
              <li>
                <a
                  href={`/subjects/${to58(subjectEntityId)}/talk`}
                  itemProp="discussionUrl"
                >
                  <Icon i="talk" s="s" /> Talk
                </a>
              </li>
              {/* <li><a href="/mocks/history">🎢 History</a></li> */}
              {/* <li><a href="/mocks/update-subject">🌳 Edit</a></li> */}
            </ul>
          </small>
          {/* TODO stats section */}
        </header>
        <ListOfSubjects
          subjects={childSubjects.nodes}
          title="What's inside?"
          icon="child"
        />
        {subjectDetails && (
          <section>
            <h2>
              More about &quot;{subjectName}&quot; <Icon s="h2" i="cheer" />
            </h2>
            <ReactMarkdown source={subjectDetails} />
          </section>
        )}
        <ListOfSubjects
          subjects={parentSubjects.nodes}
          title="Want learn more? Try one of these&hellip;"
          icon="parent"
        />
        <ListOfSubjects
          subjects={beforeSubjects.nodes}
          title="Before this we recommend&hellip;"
          icon="before"
          itemProp="coursePrerequisites"
        />
        <ListOfSubjects
          subjects={afterSubjects.nodes}
          title="Learning this gets you ready for&hellip;"
          icon="after"
        />
        {cardCount > 0 && (
          <section>
            <h2>
              {cardCount} cards <Icon i="card" s="h2" /> in &quot;{subjectName}
              &quot;
            </h2>
            <ul>
              <ListOfCards cards={cards.nodes} kind="VIDEO" />
              <ListOfCards cards={cards.nodes} kind="PAGE" />
              <ListOfCards cards={cards.nodes} kind="CHOICE" />
              <ListOfCards cards={cards.nodes} kind="UNSCORED_EMBED" />
            </ul>
            <p>
              <a href={`/create-card?subjectId=${to58(subjectEntityId)}`}>
                <Icon i="card" /> Help us make some cards
              </a>
            </p>
          </section>
        )}

        <section
          itemProp="provider"
          itemScope
          itemType="https://schema.org/EducationalOrganization"
        >
          <h2>
            Why learn about <q>{subjectName}</q> with{' '}
            <a href="/" itemProp="url">
              <span itemProp="name">Sagefy</span>
            </a>
            ? <Icon i="sagefy" s="h2" />
          </h2>
          <p>
            <em>
              Learn about <q>{subjectName}</q>, adapted for you. Free.
            </em>
          </p>
          <p>
            <Icon i="open" />{' '}
            <strong>
              Learn about <q>{subjectName}</q>.
            </strong>{' '}
            Anyone can view, share, create, and edit content. Because anyone can
            contribute, you can learn anything you want.
          </p>
          <p>
            <Icon i="adapt" /> <strong>Adapted for you.</strong> Sagefy
            optimizes learning about <q>{subjectName}</q> based on what you
            already know. Get the most out of your time and effort spent.
          </p>
        </section>
      </div>

      <Footer role={role} />
    </Layout>
  )
}

SubjectPage.propTypes = {
  hash: string.isRequired,
  role: string,
  subject: shape({
    entityId: string.isRequired,
    name: string.isRequired,
    body: string.isRequired,
    details: string,
    childSubjects: subjectsType,
    beforeSubjects: subjectsType,
    afterSubjects: subjectsType,
    parentSubjects: subjectsType,
    cardCount: number.isRequired,
    cards: cardsType,
    image: string,
  }).isRequired,
}

SubjectPage.defaultProps = {
  role: 'sg_anonymous',
}
