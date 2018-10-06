import React from 'react'
import ReactDOM from 'react-dom'
import { Provider } from 'react-redux'
import { BrowserRouter as Router } from 'react-router-dom'

import Index from './views/index'
import createStore from './state/store'

const { store } = createStore()

document.addEventListener('DOMContentLoaded', () => {
  const container = document.querySelector('.vdom')
  ReactDOM.render(
    <Provider store={store}>
      <Router basename="/c">
        <Index />
      </Router>
    </Provider>,
    container
  )
})
