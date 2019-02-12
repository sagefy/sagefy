import React from 'react'
import { StaticRouter, Route, Switch } from 'react-router-dom'
import { string } from 'prop-types'

import HomePage from './pages/HomePage'
import ContactPage from './pages/ContactPage'
import TermsPage from './pages/TermsPage'
import NotFoundPage from './pages/NotFoundPage'
import SearchSubjectsPage from './pages/SearchSubjectsPage'
import SuggestPage from './pages/SuggestPage'

export default function Index({ location }) {
  return (
    <html lang="en">
      <head>
        <meta charSet="utf-8" />
        <meta
          name="viewport"
          content="width=device-width, initial-scale=1.0"
        />
        <link rel="stylesheet" href="/sagefy.min.css" />
        <title>
          <StaticRouter context={{}} location={location}>
            <Switch>
              <Route
                path="/search-subjects"
                render={() => 'Search Subjects'}
              />
              <Route path="/suggest" render={() => 'Suggest'} />
              <Route
                path="/search-subjects"
                render={() => 'Search Subjects'}
              />
              <Route path="/contact" render={() => 'Contact'} />
              <Route path="/terms" render={() => 'Terms'} />
              <Route path="/" exact render={() => 'Home'} />
              <Route render={() => 'Not Found'} />
            </Switch>
          </StaticRouter>{' '}
          – Sagefy
        </title>
      </head>
      <body>
        <div id="top" className="page" role="document">
          <StaticRouter context={{}} location={location}>
            <Switch>
              <Route path="/suggest" component={SuggestPage} />
              <Route path="/search-subjects" component={SearchSubjectsPage} />
              <Route path="/contact" component={ContactPage} />
              <Route path="/terms" component={TermsPage} />
              <Route path="/" exact component={HomePage} />
              <Route component={NotFoundPage} />
            </Switch>
          </StaticRouter>
        </div>
      </body>
    </html>
  )
}

Index.propTypes = {
  location: string.isRequired,
}
