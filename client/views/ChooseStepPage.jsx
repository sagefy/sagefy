import React from 'react'
import { arrayOf, shape, string } from 'prop-types'
import { convertUuidToUuid58 as to58 } from 'uuid58'
import Layout from './components/Layout'
import Icon from './components/Icon'
import ChooseSubject from './components/ChooseSubject'

export default function ChooseNextPage({
  hash,
  subject: { entityId: subjectId },
  subjects,
  role,
}) {
  return (
    <Layout
      hash={hash}
      page="ChooseNextPage"
      title="Choose"
      description="-"
      canonical={`/subjects/${to58(subjectId)}`}
    >
      <header className="my-c">
        <p>
          <em>
            Let&apos;s keep it up! <Icon i="cheer" />
          </em>
        </p>
        <h1>
          What should we focus on? <Icon i="subject" s="h1" />
        </h1>
        {/* TODO copy in this section
          only goal --
            p: Right, so {goal.name}&hellip; <Icon i="cheer" />
            h1: Where should we start? <Icon i="subject" s="h1" />
          completed step --
            p: Great job with {step.name}! <Icon i="cheer" />
            h1: What's next? <Icon i="subject" s="h1" />
        */}
      </header>

      <section>
        <ChooseSubject subjects={subjects} level="step" />
        {/* TODO <p className="ta-r">
          <small>(15% learned)</small>
        </p> */}
      </section>

      <section>
        <p className="ta-r">
          <small>
            <em>Or&hellip;</em> on second thought, let&apos;s go{' '}
            {role === 'sg_anonymous' ? (
              <a href="/">
                <Icon i="home" /> Home
              </a>
            ) : (
              <a href="/dashboard">
                to the <Icon i="dashboard" /> Dashboard
              </a>
            )}
            .
          </small>
        </p>
      </section>
    </Layout>
  )
}

ChooseNextPage.propTypes = {
  hash: string.isRequired,
  subjects: arrayOf(
    shape({
      entityId: string.isRequired,
      name: string.isRequired,
      body: string.isRequired,
    })
  ).isRequired,
  subject: shape({
    entityId: string.isRequired,
  }).isRequired,
  role: string.isRequired,
}
