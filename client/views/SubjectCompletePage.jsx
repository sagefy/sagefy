import React from 'react'
import { string, shape } from 'prop-types'
import { convertUuidToUuid58 as to58 } from 'uuid58'
import Layout from './components/Layout'
import Icon from './components/Icon'
import ExternalLink from './components/ExternalLink'

export default function SubjectCompletePage({
  hash,
  role,
  subject: { name, entityId },
}) {
  return (
    <Layout
      hash={hash}
      page="SubjectCompletePage"
      title={`Hooray! You just finished ${name}`}
      description="Congratulations!"
      canonical={`/subjects/${to58(entityId)}`}
    >
      <header className="my-c">
        <p>
          <em>
            Congratulations! <Icon i="cheer" /> You just finished&hellip;
          </em>
        </p>
        <h1>
          <q>{name}</q> <Icon i="subject" s="h1" />
        </h1>
      </header>
      <section className="ta-c">
        <i className="Icon d-ib" style={{ maxWidth: '200px' }}>
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 306.976 306.976">
            <path d="M230.879 144.952c-3.426-4.771-4.874-10.757-3.84-16.786l2.061-12.018-8.73-8.51c-.133-.129-.253-.267-.382-.399-66.809 55.733-74.408 145.071-73.68 188.929a3.135 3.135 0 0 0 6.207.576c18.429-89.754 53.282-132.175 78.364-151.792zM99.861 85.018L79.7 89.531l-7.712 19.167c-.14.348-.298.685-.454 1.023 31.466 44.515 47.854 135.4 54.405 181.181a2.073 2.073 0 0 0 4.127-.279c.797-98.746-14.309-164.631-29.555-205.773-.217.054-.43.119-.65.168zM237.742 244.904l-2.857-3.93a22.348 22.348 0 0 1-4.133-10.52c-21.992 5.865-55.074 20.873-65.644 58.833a4.357 4.357 0 0 0 7.784 3.643c11.534-16.727 32.267-38.816 63.187-43.301.017-.048.029-.097.046-.146l1.617-4.579zM80.479 206.57a22.393 22.393 0 0 1-7.904 6.851l-4.309 2.241-.597 4.82a22.663 22.663 0 0 1-.943 4.21c18.465 20.857 32.072 49.507 40.295 70.078a2.906 2.906 0 0 0 5.563-1.567c-7.281-42.993-20.016-69.918-32.105-86.633zM250.59 109.166l-3.839 22.381a2.372 2.372 0 0 0 3.443 2.501l20.1-10.567 20.099 10.567a2.373 2.373 0 0 0 3.443-2.501l-3.839-22.381 16.261-15.851a2.374 2.374 0 0 0-1.315-4.048l-22.472-3.265-10.05-20.363a2.374 2.374 0 0 0-4.256 0l-10.05 20.363-22.472 3.265a2.373 2.373 0 0 0-1.316 4.048l16.263 15.851zM95.493 65.501a2.372 2.372 0 0 0 1.005-4.136L72.588 41.36l2.925-31.037a2.375 2.375 0 0 0-3.622-2.234L45.476 24.647 16.861 12.275a2.369 2.369 0 0 0-2.478.369 2.372 2.372 0 0 0-.765 2.386l7.585 30.238-20.61 23.39a2.372 2.372 0 0 0 1.619 3.936l31.102 2.131 15.877 26.829a2.374 2.374 0 0 0 4.245-.322l11.637-28.921 30.42-6.81zM302.251 235.51a2.373 2.373 0 0 0-1.616-1.915l-14.62-4.745-4.379-14.734a2.372 2.372 0 0 0-4.195-.718l-9.031 12.439-15.366-.388-.06-.001a2.373 2.373 0 0 0-1.919 3.768l9.039 12.433-5.118 14.495a2.372 2.372 0 0 0 2.972 3.047l14.618-4.755 12.204 9.346a2.374 2.374 0 0 0 3.816-1.885l-.005-15.371 12.66-8.718a2.379 2.379 0 0 0 1-2.298zM63.347 195.678a2.374 2.374 0 0 0-.09-4.256l-13.925-6.51-2.531-15.161a2.373 2.373 0 0 0-4.074-1.229l-10.494 11.232-15.202-2.278a2.371 2.371 0 0 0-2.428 3.496l7.439 13.452-6.864 13.754a2.375 2.375 0 0 0 2.574 3.39l15.092-2.918 10.96 10.778a2.372 2.372 0 0 0 4.019-1.4l1.889-15.255 13.635-7.095zM164.224 67.025l-1.845-4.493-4.748-1.027a22.386 22.386 0 0 1-9.427-4.526c-7.651 20.35-13.008 51.827-7.374 99.172.303 2.548 4.02 2.518 4.262-.036 2.083-21.962 7.451-57.474 21.156-85.27a22.545 22.545 0 0 1-2.024-3.82zM170.993 12.588l1.552 15.293-11.718 9.948a2.371 2.371 0 0 0 1.034 4.129l15.024 3.25 5.84 14.219a2.372 2.372 0 0 0 4.246.293l7.734-13.284 15.328-1.16a2.372 2.372 0 0 0 1.59-3.948l-10.244-11.46 3.633-14.936a2.372 2.372 0 0 0-3.264-2.733L187.683 18.4 174.6 10.329a2.368 2.368 0 0 0-2.506.009 2.372 2.372 0 0 0-1.101 2.25z" />
          </svg>
        </i>
        <p>Take a moment to appreciate your hard work!</p>
      </section>
      <section>
        <h2>
          What&apos;s next? <Icon i="search" s="h2" />
        </h2>
        <ul>
          <li>
            Share the subject on social media:
            <ul className="ls-n">
              <li>
                <ExternalLink
                  href={`https://twitter.com/intent/tweet?text=${encodeURIComponent(
                    `I just finished ${name} on Sagefy https://sagefy.org/subjects/${to58(
                      entityId
                    )}`
                  )}`}
                >
                  <Icon i="twitter" /> Twitter
                </ExternalLink>
              </li>
              <li>
                <ExternalLink
                  href={`https://www.facebook.com/sharer/sharer.php?u=https://sagefy.org/subjects/${to58(
                    entityId
                  )}`}
                >
                  <Icon i="facebook" /> Facebook
                </ExternalLink>
              </li>
              <li>
                <ExternalLink
                  href={`https://www.linkedin.com/sharing/share-offsite?url=https://sagefy.org/subjects/${to58(
                    entityId
                  )}`}
                >
                  <Icon i="linkedin" /> LinkedIn
                </ExternalLink>
              </li>
            </ul>
          </li>
          <li>
            <a href={`/subjects/${to58(entityId)}`}>
              Help contribute to the subject <Icon i="build" />
            </a>
          </li>
          {role === 'sg_anonymous' ? (
            <li>
              <a href="/search/subjects">
                Find your next subject <Icon i="search" />
              </a>
            </li>
          ) : (
            <li>
              <a href="/dashboard">
                Return back to your dashboard <Icon i="dashboard" />
              </a>
            </li>
          )}
        </ul>
      </section>
    </Layout>
  )
}

SubjectCompletePage.propTypes = {
  hash: string.isRequired,
  role: string,
  subject: shape({}).isRequired,
}

SubjectCompletePage.defaultProps = { role: 'sg_anonymous' }
