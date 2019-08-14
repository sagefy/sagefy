import React from 'react'
import { string, shape, arrayOf } from 'prop-types'
import get from 'lodash.get'
import { convertUuidToUuid58 as to58 } from 'uuid58'
import ReactMarkdown from 'react-markdown'
import shorten from '../util/shorten'
import Layout from './components/Layout'
import Icon from './components/Icon'
import Footer from './components/Footer'
import SubjectForm from './components/SubjectForm'
import CARD_KIND from '../util/card-kind'

export default function SearchPage({ role, query: { q }, results, hash }) {
  return (
    <Layout
      hash={hash}
      page="SearchPage"
      title="Search all of Sagefy"
      description="Find what you are looking for. Anything you want to learn, Sagefy can help you."
    >
      <section className="ta-c">
        <h1>
          What do you want to find? <Icon i="search" s="h1" />
        </h1>
        <form action="/search">
          <p>
            <input
              type="search"
              size="40"
              value={q}
              placeholder="example: Music"
              autoFocus={!!q}
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

      {results && results.length ? (
        <section>
          <h2>
            How about one of these? <Icon i="subject" s="h2" />{' '}
            <Icon i="card" s="h2" />
          </h2>
          <ul className="ls-n">
            {results.map(({ kind, subkind, entityId, name, body }) => (
              <li className="my-c">
                <small>
                  {kind === 'card' && get(CARD_KIND, [subkind, 'name'])}{' '}
                  {kind === 'card' ? 'Card' : 'Subject'}{' '}
                  {kind === 'card' && (
                    <Icon i={get(CARD_KIND, [subkind, 'icon'])} s="s" />
                  )}
                  <Icon i={kind} s="s" />
                </small>
                <h3>
                  <a
                    href={`/${
                      kind === 'card'
                        ? `${get(CARD_KIND, [subkind, 'url'])}-`
                        : ''
                    }${kind}s/${to58(entityId)}`}
                  >
                    {name}
                  </a>
                </h3>
                {kind === 'subject' && (
                  <ReactMarkdown
                    source={shorten(body)}
                    disallowedTypes={['heading']}
                  />
                )}
                {subkind === 'page' && (
                  <ReactMarkdown
                    source={shorten(body.body)}
                    disallowedTypes={['heading']}
                  />
                )}
                {subkind === 'choice' && (
                  <p>
                    {shorten(
                      Object.values(body.options)
                        .map(({ value }) => value)
                        .join(' • ')
                    )}
                  </p>
                )}
              </li>
            ))}
          </ul>
        </section>
      ) : null}

      {q ? (
        <section className="my-c">
          <p>
            <em>
              Not seeing what you want? <Icon i="error" />
            </em>
          </p>
          <details open={!results || !results.length}>
            <summary>
              <h2 className="d-i">
                You can suggest a new subject <Icon i="subject" s="h2" />
              </h2>
            </summary>
            <SubjectForm role={role} preset={{ name: q }} />
          </details>
        </section>
      ) : (
        <section>
          <h2>
            Searching on Sagefy <Icon i="search" s="h2" />
          </h2>
          <p>
            If you&apos;re wanting to learn a new subject,{' '}
            <a href="/subjects/search">search just subjects instead</a>.
          </p>
          <p>
            On this page, you can search for cards and subjects across Sagefy.
            Wanting to see everything Sagefy has on a topic? Found something
            that needs an edit? Do you want to make some new cards? You&apos;re
            in the right place.
          </p>
        </section>
      )}

      <Footer role={role} />
    </Layout>
  )
}

SearchPage.propTypes = {
  hash: string.isRequired,
  role: string,
  query: shape({}).isRequired,
  results: arrayOf(
    shape({
      entityId: string.isRequired,
      name: string.isRequired,
      body: string.isRequired,
    })
  ),
}

SearchPage.defaultProps = {
  role: 'sg_anonymous',
  results: [],
}
