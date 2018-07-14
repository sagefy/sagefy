import React from 'react'
import ReactDOM from 'react-dom'
import { createStore } from 'redux'
import { Provider } from 'react-redux'

import Index from './views/Index'

const store = createStore((a = {}) => a)

document.addEventListener('DOMContentLoaded', () => {
  const container = document.querySelector('.vdom')
  ReactDOM.render(
    <Provider store={store}>
      <Index />
    </Provider>,
    container
  )
})

/* const { createStore, applyMiddleware, bindActionCreators } = require('redux')
const createReduxListen = require('redux-listen')
const { createReducer, createActions /* createActionTypes } = require('redux-schemad')
const { stateSchema } = require('./state/stateSchema')

const reducer = createReducer(stateSchema)
const listenStore = createReduxListen()
const store = createStore(reducer, applyMiddleware(listenStore))
const actions = bindActionCreators(createActions(stateSchema), store.dispatch)
// const actionTypes = createActionTypes(stateSchema)
*/
