import React from 'react'
import { Route } from 'react-router-dom'
import HomePage from './pages/Home'

export default function IndexView() {
  return (
    <Route path="/c">
      <Route path="/" component={HomePage} />
    </Route>
  )
}
