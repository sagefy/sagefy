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
import VideoCardPage from './pages/VideoCardPage'
import PageCardPage from './pages/PageCardPage'
import UnscoredEmbedCardPage from './pages/UnscoredEmbedCardPage'
import ChoiceCardPage from './pages/ChoiceCardPage'
import UserPage from './pages/UserPage'
import TalkPage from './pages/TalkPage'

export default function Index(props) {
  const { url } = props
  const withProps = component => () => React.createElement(component, props)
  return (
    <StaticRouter context={{}} location={url}>
      <Switch>
        <Route path="/users/:userId" render={withProps(UserPage)} />
        <Route path="/:kind-cards/:cardId/talk" render={withProps(TalkPage)} />
        <Route path="/video-cards/:cardId" render={withProps(VideoCardPage)} />
        <Route path="/page-cards/:cardId" render={withProps(PageCardPage)} />
        <Route
          path="/unscored-embed-cards/:cardId"
          render={withProps(UnscoredEmbedCardPage)}
        />
        <Route
          path="/choice-cards/:cardId"
          render={withProps(ChoiceCardPage)}
        />
        <Route path="/subjects/:subjectId/talk" render={withProps(TalkPage)} />
        <Route path="/subjects/:subjectId" render={withProps(SubjectPage)} />
        <Route path="/choose-step" render={withProps(ChooseStepPage)} />
        <Route path="/learn-video/:cardId" render={withProps(LearnVideoPage)} />
        <Route path="/learn-page/:cardId" render={withProps(LearnPagePage)} />
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
        <Route path="/search-subjects" render={withProps(SearchSubjectsPage)} />
        <Route path="/create-subject" render={withProps(CreateSubjectPage)} />
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
  )
}

Index.propTypes = {
  url: string.isRequired,
}
