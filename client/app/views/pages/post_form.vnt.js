const broker = require('../../modules/broker')
const tasks = require('../../modules/tasks')
const { getFormValues, parseFormValues } = require('../../modules/auxiliaries')

module.exports = broker.add({
  'submit #post-form.create form'(e, el) {
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
        values.post.entity_version
        && values.post.entity_version.kind) {
        values[values.post.entity_version.kind] = values.entity
        delete values.entity
      }
    } */
    tasks.createPost(values)
  },

  'submit #post-form.update form'(e, el) {
    if (e) {
      e.preventDefault()
    }
    let values = getFormValues(el)
    tasks.updateFormData(values)
    // errors = tasks.validateForm(values, schema, [...])
    // unless errors?.length, (...tab)
    values = parseFormValues(values)
    tasks.updatePost(values)
  },
})
