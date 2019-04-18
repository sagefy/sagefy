import React from 'react'
import { shape, string, instanceOf, arrayOf } from 'prop-types'
import Layout from '../components/Layout'
import Icon from '../components/Icon'
import ListOfSubjects from '../components/ListOfSubjects'
import ListOfCards from '../components/ListOfCards'

export default function UserPage({
  hash,
  user: {
    name: userName,
    md5Email,
    created: userCreated,
    subjectVersionsByUserId,
    cardVersionsByUserId,
  },
}) {
  return (
    <Layout
      hash={hash}
      page="UserPage"
      title={userName}
      description={`Joined ${userCreated.slice(0, 10)}`}
    >
      <header>
        <div className="m-yc">
          <p>
            User <Icon i="user" />
          </p>
          <h1>{userName}</h1>
        </div>
        <table>
          <tr>
            <td>
              <img
                src={`https://www.gravatar.com/avatar/${md5Email}?d=mm&amp;s=120`}
                alt="gravatar"
              />
            </td>
            <td>
              <p>Here is my bio text. I am an interesting person.</p>
              <p>
                <small>Joined {userCreated.slice(0, 10)}</small>
              </p>
            </td>
          </tr>
        </table>
        {/* <small>
    <ul class="ls-i ta-r">
      <li><a href="/mocks/follows">👂🏿 Follow</a></li>
      <li><a href="/mocks/talk">💬 Talk</a></li>
      <li><a href="/mocks/settings">🛠 Settings</a></li>
      <!-- if self -->
    </ul>
  </small> */}
        {/* TODO stats */}
      </header>

      <section>
        <hr />
        <h2>
          How I helped build Sagefy <Icon i="cheer" s="xl" />
        </h2>
        <hr />
      </section>
      {subjectVersionsByUserId.nodes.length ? (
        <section>
          <ListOfSubjects
            subjects={subjectVersionsByUserId.nodes}
            title="Subject versions I made"
            icon="subject"
          />
        </section>
      ) : null}

      {cardVersionsByUserId.nodes.length ? (
        <section>
          <h2>
            Card versions I made <Icon i="card" s="l" />
          </h2>
          <ul>
            <ListOfCards cards={cardVersionsByUserId.nodes} kind="VIDEO" />
            <ListOfCards cards={cardVersionsByUserId.nodes} kind="PAGE" />
            <ListOfCards cards={cardVersionsByUserId.nodes} kind="CHOICE" />
            <ListOfCards
              cards={cardVersionsByUserId.nodes}
              kind="UNSCORED_EMBED"
            />
          </ul>
        </section>
      ) : null}

      {/* TODO posts and topics */}
    </Layout>
  )
}

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

UserPage.propTypes = {
  hash: string.isRequired,
  user: shape({
    name: string.isRequired,
    md5Email: string.isRequired,
    created: instanceOf(Date).isRequired,
    subjectVersionsByUserId: shape({
      nodes: subjectsType,
    }),
    cardVersionsByUserId: shape({
      nodes: cardsType,
    }),
  }).isRequired,
}

/*
<!-- Only if user enables in settings... -->
<section>
  <h2>What I'm learning 🏆</h2>
  <table>
    <tr>
      <td class="ta-c m-yc">
        <p><button>👍</button></p>
        <pre><small>12 fans</small></pre>
      </td>
      <td class="m-yc">
        <h3>
          <a href="/mocks/choose-next"
            >🎧 An Introduction to Electronic Music</a
          >
        </h3>
        <!-- This should immediately launch the learning experience! -->
        <p>
          A small taste of the basics of electronic music. Learn the concepts
          behind creating and modifying sounds in an electronic music system.
          Learn the ideas behind the tools and systems we use to create
          electronic music.
        </p>
      </td>
    </tr>
  </table>
</section>
*/
