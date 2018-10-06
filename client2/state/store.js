import createReduxListen from 'redux-listen'
import { configureStore, createReducer } from '@acemarke/redux-starter-kit'
import {
  createDefaultState,
  createSchemadReducer,
  createActionTypes,
  createActions,
  verifyStateKeysMiddleware,
} from 'redux-schemad'
import { schema } from './schema'

const actions = createActions(schema)
const actionTypes = createActionTypes(schema)
const reducer = createSchemadReducer(schema, createReducer)
const defaultState = createDefaultState(schema)
const verify = verifyStateKeysMiddleware(schema)

export default function createStore() {
  const listenStore = createReduxListen()
  return {
    listenStore,
    actions,
    actionTypes,
    store: configureStore({
      reducer,
      middleware: [listenStore.middleware, verify],
      preloadedState:
        (typeof window !== 'undefined' && window.preload) || defaultState,
    }),
  }
}
