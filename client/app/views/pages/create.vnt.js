const broker = require('../../helpers/broker')
const tasks = require('../../helpers/tasks')
const { getFormValues, parseFormValues } = require('../../helpers/forms')
const subjectSchema = require('../../schemas/subject')
const unitSchema = require('../../schemas/unit')
const cardSchema = require('../../schemas/card')
const { closest } = require('../../helpers/utilities')

module.exports = broker.add({
  'click .create__route'(e, el) {
    if (e) e.preventDefault()
    const [, , kind, step] = el.pathname.split('/')
    tasks.resetCreate()
    tasks.updateCreateRoute({ kind, step })
  },

  'submit .create--subject-create form'(e, el) {
    if (e) e.preventDefault()
    let values = getFormValues(el)
    values = parseFormValues(values)
    const errors = tasks.validateForm(values, subjectSchema, [
      'name',
      'language',
      'body',
      'members',
    ])
    if (errors && errors.length) {
      return
    }
    const data = {
      topic: {
        name: `Create a Subject: ${values.name}`,
        entity_id: '1rk0jS5EGEavSG4NBxRvPkZf',
        entity_kind: 'unit',
      },
      post: {
        kind: 'proposal',
        body: `Create a Subject: ${values.name}`,
      },
      subject: {
        name: values.name,
        body: values.body,
        members: values.members,
      },
    }
    tasks.createSubjectProposal(data)
  },

  'submit .create--unit-create form'(e, el) {
    if (e) e.preventDefault()
    let values = getFormValues(el)
    values = parseFormValues(values)
    values.require_ids =
      (values.require_ids && values.require_ids.map(rmap => rmap.id)) || []
    const errors = tasks.validateForm(values, unitSchema, [
      'name',
      'language',
      'body',
      'require_ids',
    ])
    if (errors && errors.length) {
      return
    }
    tasks.addMemberToAddUnits(values)
    tasks.route('/create/unit/list')
  },

  'submit .create--subject-add__form'(e, el) {
    if (e) e.preventDefault()
    const q = el.querySelector('input').value
    tasks.search({ q, kind: 'unit,subject' })
  },

  'submit .create--unit-add__form'(e, el) {
    if (e) e.preventDefault()
    const q = el.querySelector('input').value
    tasks.search({ q, kind: 'unit' })
  },

  'click .create--subject-add__add'(e, el) {
    if (e) e.preventDefault()
    const { kind, id, name, body } = el.dataset
    tasks.addMemberToCreateSubject({ kind, id, name, body })
  },

  'click .create--unit-add__add'(e, el) {
    if (e) e.preventDefault()
    const { id, name, body, version } = el.dataset
    tasks.addMemberToAddUnits({ id, name, body, version })
  },

  'click .create--subject-create .form-field--entities__a'(e, el) {
    if (e) e.preventDefault()
    const form = closest(el, 'form')
    const values = getFormValues(form)
    tasks.createSubjectData(values)
    tasks.route('/create/subject/add')
  },

  'click .create--unit-create .form-field--entities__a'(e, el) {
    if (e) e.preventDefault()
    const form = closest(el, 'form')
    let values = getFormValues(form)
    values = parseFormValues(values)
    tasks.stowProposedUnit(values)
    tasks.route('/create/unit/create/add')
  },

  'click .create--subject-create .form-field--entities__remove'(e, el) {
    if (e) e.preventDefault()
    const { id } = el
    tasks.removeMemberFromCreateSubject({ id })
  },

  'click .create--unit-find__choose'(e, el) {
    if (e) e.preventDefault()
    const { id, name } = el.dataset
    tasks.createChooseSubjectForUnits({ id, name })
  },

  'submit .create--unit-find__form'(e, el) {
    if (e) e.preventDefault()
    const q = el.querySelector('input').value
    tasks.search({ q, kind: 'subject' })
  },

  'click .create--card-find__choose'(e, el) {
    if (e) e.preventDefault()
    const { id, name } = el.dataset
    tasks.createChooseUnitForCards({ id, name })
  },

  'submit .create--card-find__form'(e, el) {
    if (e) e.preventDefault()
    const q = el.querySelector('input').value
    tasks.search({ q, kind: 'unit' })
  },

  'submit .create--unit-create-add__form'(e, el) {
    if (e) e.preventDefault()
    const q = el.querySelector('input').value
    tasks.search({ q, kind: 'unit' })
  },

  'click .create--unit-create-add__add'(e, el) {
    if (e) e.preventDefault()
    const { id, name, body } = el.dataset
    tasks.addRequireToProposedUnit({ id, name, body, kind: 'unit' })
  },

  'click .create--unit-list__remove'(e, el) {
    if (e) e.preventDefault()
    const { index } = el.dataset
    tasks.removeUnitFromSubject({ index })
  },

  'click .create--unit-list__submit'(e) {
    if (e) e.preventDefault()
    tasks.createUnitsProposal()
  },

  'click .create--card-list__remove'(e, el) {
    if (e) e.preventDefault()
    const { index } = el.dataset
    tasks.removeCardFromUnit({ index })
  },

  'click .create--card-list__submit'(e) {
    if (e) e.preventDefault()
    tasks.createCardsProposal()
  },

  'change .create--card-create [name="kind"]'(e, el) {
    const form = closest(el, 'form')
    const values = getFormValues(form)
    tasks.stowProposedCard(values)
  },

  'submit .create--card-create form'(e, el) {
    if (e) e.preventDefault()
    let values = getFormValues(el)
    values = parseFormValues(values)
    const errors = tasks.validateForm(values, cardSchema, [
      'name',
      'language',
      'kind',
    ])
    if (errors && errors.length) {
      return
    }
    tasks.addMemberToAddCards(values)
    tasks.route('/create/card/list')
  },
})
