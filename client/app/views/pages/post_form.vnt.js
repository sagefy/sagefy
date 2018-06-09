const { getFormValues, parseFormValues } = require('../../helpers/forms')

module.exports = (store, broker) => {
  const { getTasks } = store
  broker.add({
    'submit #post-form.create form'(e, el) {
      if (e) {
        e.preventDefault()
      }
      let values = getFormValues(el)
      getTasks().updateFormData(values)
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
      getTasks().createPost(values)
    },

    'submit #post-form.update form'(e, el) {
      if (e) {
        e.preventDefault()
      }
      let values = getFormValues(el)
      getTasks().updateFormData(values)
      // errors = tasks.validateForm(values, schema, [...])
      // unless errors?.length, (...tab)
      values = parseFormValues(values)
      getTasks().updatePost(values)
    },
  })
}
