import React from 'react'
import { Route, Switch } from 'react-router-dom'

import MySubjectsPage from './pages/MySubjectsPage'
import RecommendedSubjectsPage from './pages/RecommendedSubjectsPage'
import ChooseUnitPage from './pages/ChooseUnitPage'
import LearnCardPage from './pages/LearnCardPage'

import CreateSubjectCreatePage from './pages/CreateSubjectCreatePage'
import CreateSubjectAddPage from './pages/CreateSubjectAddPage'
import CreateUnitFindPage from './pages/CreateUnitFindPage'
import CreateUnitListPage from './pages/CreateUnitListPage'
import CreateUnitAddPage from './pages/CreateUnitAddPage'
import CreateUnitCreateAddPage from './pages/CreateUnitCreateAddPage'
import CreateUnitCreatePage from './pages/CreateUnitCreatePage'
import CreateCardFindPage from './pages/CreateCardFindPage'
import CreateCardListPage from './pages/CreateCardListPage'
import CreateCardCreatePage from './pages/CreateCardCreatePage'
import CreatePage from './pages/CreatePage'

import NoticesPage from './pages/NoticesPage'
import FollowsPage from './pages/FollowsPage'

import SignUpPage from './pages/SignUpPage'
import LogInPage from './pages/LogInPage'
import PasswordPage from './pages/PasswordPage'
import SettingsPage from './pages/SettingsPage'

import TopicPage from './pages/TopicPage'
import CreateTopicPage from './pages/CreateTopicPage'
import UpdateTopicPage from './pages/UpdateTopicPage'
import CreatePostPage from './pages/CreatePostPage'
import UpdatePostPage from './pages/UpdatePostPage'

import CardPage from './pages/CardPage'
import UnitPage from './pages/UnitPage'
import SubjectPage from './pages/SubjectPage'
import SubjectTreePage from './pages/SubjectTreePage'
import SubjectLandingPage from './pages/SubjectLandingPage'
import CardVersionsPage from './pages/CardVersionsPage'
import UnitVersionsPage from './pages/UnitVersionsPage'
import SubjectVersionsPage from './pages/SubjectVersionsPage'
import ProfilePage from './pages/ProfilePage'

import SuggestPage from './pages/SuggestPage'
import SearchPage from './pages/SearchPage'
import ContactPage from './pages/ContactPage'
import TermsPage from './pages/TermsPage'
import HomePage from './pages/HomePage'
import ErrorPage from './pages/ErrorPage'

import Menu from './components/Menu'

export default function IndexView() {
  return (
    <main>
      <Switch>
        <Route path="/my_subjects" component={MySubjectsPage} />
        <Route
          path="/recommended_subjects"
          component={RecommendedSubjectsPage}
        />
        <Route
          path="/subjects/:subjectId/choose_unit"
          component={ChooseUnitPage}
        />
        <Route path="/cards/:cardId/learn" component={LearnCardPage} />

        <Route
          path="/create/subject/create"
          component={CreateSubjectCreatePage}
        />
        <Route path="/create/subject/add" component={CreateSubjectAddPage} />
        <Route path="/create/unit/find" component={CreateUnitFindPage} />
        <Route path="/create/unit/list" component={CreateUnitListPage} />
        <Route path="/create/unit/add" component={CreateUnitAddPage} />
        <Route
          path="/create/unit/create/add"
          component={CreateUnitCreateAddPage}
        />
        <Route path="/create/unit/create" component={CreateUnitCreatePage} />
        <Route path="/create/card/find" component={CreateCardFindPage} />
        <Route path="/create/card/list" component={CreateCardListPage} />
        <Route path="/create/card/create" component={CreateCardCreatePage} />
        <Route path="/create" component={CreatePage} />

        <Route path="/notices" component={NoticesPage} />
        <Route path="/follows" component={FollowsPage} />

        <Route path="/sign_up" component={SignUpPage} />
        <Route path="/log_in" component={LogInPage} />
        <Route path="/password" component={PasswordPage} />
        <Route path="/settings" component={SettingsPage} />

        <Route path="/topics/:topicId" component={TopicPage} />
        <Route path="/topics/create" component={CreateTopicPage} />
        <Route path="/topics/:topicId/update" component={UpdateTopicPage} />
        <Route
          path="/topics/:topicId/posts/create"
          component={CreatePostPage}
        />
        <Route
          path="/topics/:topicId/posts/:postId/update"
          component={UpdatePostPage}
        />

        <Route path="/cards/:cardId" component={CardPage} />
        <Route path="/units/:unitId" component={UnitPage} />
        <Route path="/subjects/:subjectId" component={SubjectPage} />
        <Route path="/subjects/:subjectId/tree" component={SubjectTreePage} />
        <Route
          path="/subjects/:subjectId/landing"
          component={SubjectLandingPage}
        />
        <Route path="/cards/:cardId/versions" component={CardVersionsPage} />
        <Route path="/units/:unitId/versions" component={UnitVersionsPage} />
        <Route
          path="/subjects/:subjectId/versions"
          component={SubjectVersionsPage}
        />
        <Route path="/users/:userId" component={ProfilePage} />

        <Route path="/suggest" component={SuggestPage} />
        <Route path="/search" component={SearchPage} />
        <Route path="/contact" component={ContactPage} />
        <Route path="/terms" component={TermsPage} />
        <Route exact path="/" component={HomePage} />
        <Route component={ErrorPage} />
      </Switch>
      <Menu />
    </main>
  )
}

/*

// Do nothing on empty links
'click a[href="#"]': e => {
  e.preventDefault()
},

// Open external URLs in new windows
'click a[href*="//"]': (e, el) => {
  el.target = '_blank'
},
*/
