import React from 'react'
import { StaticRouter, Route, Switch } from 'react-router-dom'
import { string, shape } from 'prop-types'

import HomePage from './pages/HomePage'
import ContactPage from './pages/ContactPage'
import TermsPage from './pages/TermsPage'
import NotFoundPage from './pages/NotFoundPage'
import SearchSubjectsPage from './pages/SearchSubjectsPage'
import SignUpPage from './pages/SignUpPage'
import DashboardPage from './pages/DashboardPage'
import ServerErrorPage from './pages/ServerErrorPage'
import LogInPage from './pages/LogInPage'
import PasswordPage from './pages/PasswordPage'
import EmailPage from './pages/EmailPage'
import SettingsPage from './pages/SettingsPage'

export const output = a => () => a
const searchSubjects = output('Search Subjects')
const contact = output('Contact')
const terms = output('Terms')
const home = output('Home')
const notFound = output('Not Found')
const signUp = output('Sign Up')
const dashboard = output('Dashboard')
const serverError = output('Server Error')
const logIn = output('Log In')
const password = output('Password')
const email = output('Email')
const settings = output('Settings')

export default function Index(props) {
  const { location, cacheHash } = props
  return (
    <html lang="en">
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <link rel="stylesheet" href={`/sagefy.min.css?${cacheHash}`} />
        <title>
          <StaticRouter context={{}} location={location}>
            <Switch>
              <Route path="/log-in" render={logIn} />
              <Route path="/password" render={password} />
              <Route path="/email" render={email} />
              <Route path="/settings" render={settings} />
              <Route path="/dashboard" render={dashboard} />
              <Route path="/sign-up" render={signUp} />
              <Route path="/search-subjects" render={searchSubjects} />
              <Route path="/contact" render={contact} />
              <Route path="/terms" render={terms} />
              <Route path="/server-error" render={serverError} />
              <Route path="/" exact render={home} />
              <Route render={notFound} />
            </Switch>
          </StaticRouter>{' '}
          – Sagefy
        </title>
      </head>
      <body>
        <div id="top" className="page" role="document">
          <StaticRouter context={{}} location={location}>
            <Switch>
              <Route path="/log-in" render={() => <LogInPage {...props} />} />
              <Route
                path="/password"
                render={() => <PasswordPage {...props} />}
              />
              <Route path="/email" render={() => <EmailPage {...props} />} />
              <Route
                path="/settings"
                render={() => <SettingsPage {...props} />}
              />
              <Route path="/dashboard" component={DashboardPage} />
              <Route path="/sign-up" render={() => <SignUpPage {...props} />} />
              <Route path="/search-subjects" component={SearchSubjectsPage} />
              <Route path="/contact" component={ContactPage} />
              <Route path="/terms" component={TermsPage} />
              <Route path="/server-error" render={ServerErrorPage} />
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
  cacheHash: string.isRequired,
  gqlErrors: shape({}),
  prevValues: shape({}),
}

Index.defaultProps = {
  gqlErrors: {},
  prevValues: {},
}
