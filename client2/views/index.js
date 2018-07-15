import React from 'react'
import { Route, Switch } from 'react-router-dom'
import HomePage from './pages/Home'
import TermsPage from './pages/Terms'
import ContactPage from './pages/Contact'

export default function IndexView() {
  return (
    <main>
      <Switch>
        <Route path="/contact" component={ContactPage} />
        <Route path="/terms" component={TermsPage} />
        <Route exact path="/" component={HomePage} />
      </Switch>
    </main>
  )
}
