import React from 'react'
import { BrowserRouter as Router, Route } from 'react-router-dom'
import HomePage from './pages/Home'

export default function IndexView() {
  return (
    <Router>
      <Route exact path="/" component={HomePage} />
    </Router>
  )
}
