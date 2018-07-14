import { createStore, applyMiddleware } from 'redux'
import createReduxListen from 'redux-listen'
import { createReducer, createActions, createActionTypes } from 'redux-schemad'
import stateSchema from '../state/stateSchema'

export const reducer = createReducer(stateSchema)
export const actionTypes = createActionTypes(stateSchema)
export const actions = createActions(stateSchema)

export default function createSagefyStore() {
  const listenStore = createReduxListen()
  return createStore(reducer, applyMiddleware(listenStore.middleware))
}
