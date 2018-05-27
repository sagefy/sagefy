const broker = require('../../helpers/broker')
const tasks = require('../../helpers/tasks')
const { closest } = require('../../helpers/utilities')
const { getFormValues, parseFormValues } = require('../../helpers/auxiliaries')

module.exports = broker.add({
  'submit #topic-form.create form'(e, el) {
    if (e) {
      e.preventDefault()
    }
    let values = getFormValues(el)
    tasks.updateFormData(values)
    // errors = tasks.validateForm(values, schema, [...])
    // unless errors?.length, (...tab)
    values = parseFormValues(values)
    /* PP@ if (values.post && values.post.kind === 'proposal') {
      if (values.entity && values.entity.require_ids) {
        values.entity.require_ids = values.entity.require_ids
          .map((require) => require.id).filter((require) => require)
      }
      if (values.post &&
        values.post.entity_version &&
        values.post.entity_version.kind) {
        values[values.post.entity_version.kind] = values.entity
        delete values.entity
      }
    } */
    tasks.createTopicWithPost(values)
  },

  'submit #topic-form.update form'(e, el) {
    if (e) {
      e.preventDefault()
    }
    let values = getFormValues(el)
    tasks.updateFormData(values)
    // errors = tasks.validateForm(values, schema, [...])
    // unless errors?.length, (...tab)
    values = parseFormValues(values)
    tasks.updateTopic(values)
  },

  'change #topic-form.create [name="post.kind"]'(e, el) {
    const form = closest(el, 'form')
    const values = getFormValues(form)
    tasks.updateFormData(values)
  },

  'change #topic-form.create [name="post.entity_version.kind"]'(e, el) {
    const form = closest(el, 'form')
    const values = getFormValues(form)
    tasks.updateFormData(values)
  },

  'change #topic-form.create [name="entity_kind"]'(e, el) {
    const form = closest(el, 'form')
    const values = getFormValues(form)
    tasks.updateFormData(values)
  },
})
