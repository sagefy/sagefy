/* hyperapp actions */
const mapValues = require('lodash.mapvalues')
const transform = require('lodash.transform')
const capitalize = require('lodash.capitalize')
const isPlainObject = require('lodash.isplainobject')
const omit = require('lodash.omit')
const get = require('lodash.get')
const compact = require('lodash.compact')

const FIELD = 'FIELD'
const COLLECTION = 'COLLECTION'

function field(rules, defaultValue) {
  return { type: FIELD, rules, defaultValue }
}

function collection(onField, fields) {
  return { type: COLLECTION, onField, fields }
}

function getDefault({ type, defaultValue }) {
  return {
    [FIELD]: defaultValue,
    [COLLECTION]: {},
  }[type]
}

function createDefaultState(schema) {
  return mapValues(schema, getDefault)
}

function setField(key) {
  return (state, value) => ({ [key]: value })
}

function updateField(key) {
  return (state, value) =>
    isPlainObject(state[key]) && isPlainObject(value)
      ? { [key]: { ...state[key], ...value } }
      : { [key]: value }
}

function resetField(key, defaultValue) {
  return () => ({ [key]: defaultValue })
}

function addChild(key, onField) {
  return (state, child) => ({
    [key]: {
      ...state[key],
      [child[onField]]: omit(child, onField),
    },
  })
}

function addChildren(key, onField) {
  const sub = addChild(key, onField)
  return (state, children) =>
    children.reduce((sum, child) => sub(child)(sum), state)
}

function updateChild(key, onField) {
  return (state, child) => ({
    [key]: {
      ...state[key],
      [child[onField]]: {
        ...get(state[key], child[onField], {}),
        ...omit(child, onField),
      },
    },
  })
}

function updateChildren(key, onField) {
  const sub = updateChild(key, onField)
  return (state, children) =>
    children.reduce((sum, child) => sub(child)(sum), state)
}

function removeChild(key, onField) {
  return (state, child) => ({
    [key]: omit(state[key], child[onField]),
  })
}

function removeChildren(key, onField) {
  return (state, children) => ({
    [key]: omit(state[key], children.map(child => child[onField])),
  })
}

function resetChildren(key) {
  return () => ({ [key]: {} })
}

function createFieldActions(key, { defaultValue }) {
  const name = capitalize(key)
  return {
    [`set${name}`]: setField(key),
    [`update${name}`]: updateField(key),
    [`reset${name}`]: resetField(key, defaultValue),
  }
}

function createCollectionActions(key, { onField }) {
  const one = capitalize(key.replace(/s$/, ''))
  const many = capitalize(key)
  return {
    [`add${one}`]: addChild(key, onField),
    [`add${many}`]: addChildren(key, onField),
    [`update${one}`]: updateChild(key, onField),
    [`update${many}`]: updateChildren(key, onField),
    [`remove${one}`]: removeChild(key, onField),
    [`remove${many}`]: removeChildren(key, onField),
    [`reset${many}`]: resetChildren(key),
  }
}

const TYPE_TO_ACTION_FN = {
  [FIELD]: createFieldActions,
  [COLLECTION]: createCollectionActions,
}

function createActions(schema) {
  return transform(
    schema,
    (sum, entity, key) =>
      Object.assign(sum, TYPE_TO_ACTION_FN[entity.type](key, entity)),
    {}
  )
}

function findFieldErrors({ rules }, value) {
  return compact(rules.map(value))
}

function findCollectionErrors({ onField, fields }, children) {
  return transform(
    children,
    (sum1, child, key) =>
      sum1.push(
        ...transform(
          fields,
          (sum2, { rules }, fieldKey) =>
            sum2.push(
              ...findFieldErrors(
                { rules },
                fieldKey === onField ? key : child[fieldKey]
              )
            ),
          []
        )
      ),
    []
  )
}

const TYPE_TO_CHECK = {
  [FIELD]: findFieldErrors,
  [COLLECTION]: findCollectionErrors,
}

function findStateErrors(schema, state) {
  return transform(
    schema,
    (sum, entity, key) =>
      sum.push(...TYPE_TO_CHECK[entity.type](entity, state[key])),
    []
  )
}

module.exports = {
  field,
  collection,
  createDefaultState,
  createActions,
  findStateErrors,
}
