import React from 'react'
import { StaticRouter, Route, Switch } from 'react-router-dom'
import { string } from 'prop-types'

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
import CreateSubjectPage from './pages/CreateSubjectPage'
import CreateCardPage from './pages/CreateCardPage'
import LearnChoicePage from './pages/LearnChoicePage'
import LearnPagePage from './pages/LearnPagePage'
import LearnUnscoredEmbedPage from './pages/LearnUnscoredEmbedPage'
import LearnVideoPage from './pages/LearnVideoPage'
import ChooseStepPage from './pages/ChooseStepPage'
import CreateChoiceCardPage from './pages/CreateChoiceCardPage'
import CreatePageCardPage from './pages/CreatePageCardPage'
import CreateVideoCardPage from './pages/CreateVideoCardPage'
import CreateUnscoredEmbedCardPage from './pages/CreateUnscoredEmbedCardPage'
import SubjectPage from './pages/SubjectPage'

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
const createSubject = output('Create Subject')
const createCard = output('Create Card')
const learn = output('Learn')
const chooseStep = output('Choose Step')
const subject = output('Subject')

export default function Index(props) {
  const { url, cacheHash } = props
  const withProps = component => () => React.createElement(component, props)
  return (
    <html lang="en">
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <link rel="stylesheet" href={`/sagefy.min.css?${cacheHash}`} />
        <title>
          <StaticRouter context={{}} location={url}>
            <Switch>
              <Route path="/subjects/:subjectId" render={subject} />
              <Route path="/choose-step" render={chooseStep} />
              <Route path="/learn-:type/:cardId" render={learn} />
              <Route path="/log-in" render={logIn} />
              <Route path="/password" render={password} />
              <Route path="/email" render={email} />
              <Route path="/settings" render={settings} />
              <Route path="/dashboard" render={dashboard} />
              <Route path="/sign-up" render={signUp} />
              <Route path="/search-subjects" render={searchSubjects} />
              <Route path="/create-subject" render={createSubject} />
              <Route path="/create-card" render={createCard} />
              <Route path="/create-:type-card" render={createCard} />
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
          <StaticRouter context={{}} location={url}>
            <Switch>
              <Route
                path="/subjects/:subjectId"
                render={withProps(SubjectPage)}
              />
              <Route path="/choose-step" render={withProps(ChooseStepPage)} />
              <Route
                path="/learn-video/:cardId"
                render={withProps(LearnVideoPage)}
              />
              <Route
                path="/learn-page/:cardId"
                render={withProps(LearnPagePage)}
              />
              <Route
                path="/learn-unscored-embed/:cardId"
                render={withProps(LearnUnscoredEmbedPage)}
              />
              <Route
                path="/learn-choice/:cardId"
                render={withProps(LearnChoicePage)}
              />
              <Route path="/log-in" render={withProps(LogInPage)} />
              <Route path="/password" render={withProps(PasswordPage)} />
              <Route path="/email" render={withProps(EmailPage)} />
              <Route path="/settings" render={withProps(SettingsPage)} />
              <Route path="/dashboard" render={withProps(DashboardPage)} />
              <Route path="/sign-up" render={withProps(SignUpPage)} />
              <Route
                path="/search-subjects"
                render={withProps(SearchSubjectsPage)}
              />
              <Route
                path="/create-subject"
                render={withProps(CreateSubjectPage)}
              />
              <Route path="/create-card" render={withProps(CreateCardPage)} />
              <Route
                path="/create-choice-card"
                render={withProps(CreateChoiceCardPage)}
              />
              <Route
                path="/create-page-card"
                render={withProps(CreatePageCardPage)}
              />
              <Route
                path="/create-video-card"
                render={withProps(CreateVideoCardPage)}
              />
              <Route
                path="/create-unscored-embed-card"
                render={withProps(CreateUnscoredEmbedCardPage)}
              />
              <Route path="/contact" component={ContactPage} />
              <Route path="/terms" component={TermsPage} />
              <Route path="/server-error" component={ServerErrorPage} />
              <Route path="/" exact component={withProps(HomePage)} />
              <Route component={NotFoundPage} />
            </Switch>
          </StaticRouter>
        </div>
      </body>
    </html>
  )
}

Index.propTypes = {
  url: string.isRequired,
  cacheHash: string.isRequired,
}
