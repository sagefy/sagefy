/*

const { div, h1, p, a, ul, li, small } = require('../../helpers/tags')
const info = require('../components/entity_info.tmpl')
const icon = require('../components/icon.tmpl')
const spinner = require('../components/spinner.tmpl')
const { getIsLoggedIn } = require('../../selectors/base')
const goLogin = require('../../helpers/go_login')

module.exports = data => {
  if (getIsLoggedIn(data) === null) {
    return spinner()
  }

  if (!getIsLoggedIn(data)) {
    return goLogin()
  }

  return div(
    { id: 'create', className: 'page' },
    h1('Create Cards, Units, and Subjects'),
    ul(
      { className: 'create__options' },
      li(
        a(
          {
            className: 'create__route ',
            href: '/create/subject/create',
          },
          icon('subject'),
          ' Create a Subject'
        ),
        ' Start here. ',
        small(
          ' (You can add existing units and ',
          'subjects to the new subject.)'
        )
      ),
      li(
        a(
          { className: 'create__route', href: '/create/unit/find' },
          icon('unit'),
          ' Add Units'
        ),
        ' to an existing subject.'
      ),
      li(
        a(
          { className: 'create__route', href: '/create/card/find' },
          icon('card'),
          ' Add Cards'
        ),
        ' to an existing unit.'
      )
    ),
    info(),
    p(
      'Do you want to change an existing card, unit, or subject? ',
      a({ href: '/search' }, icon('search'), ' Search for it, then click edit'),
      '.'
    )
  )
}





const { getFormValues, parseFormValues } = require('../../helpers/forms')
const subjectSchema = require('../../schemas/subject')
const unitSchema = require('../../schemas/unit')
const cardSchema = require('../../schemas/card')
const closest = require('../../helpers/closest')

module.exports = (store, broker) => {
  const { getTasks } = store

  broker.add({
    'click .create__route'(e, el) {
      if (e) e.preventDefault()
      const [, , kind, step] = el.pathname.split('/')
      getTasks().resetCreate()
      getTasks().updateCreateRoute({ kind, step })
    },

    'submit .create--subject-create form'(e, el) {
      if (e) e.preventDefault()
      let values = getFormValues(el)
      values = parseFormValues(values)
      const errors = getTasks().validateForm(values, subjectSchema, [
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
      getTasks().createSubjectProposal(data)
    },

    'submit .create--unit-create form'(e, el) {
      if (e) e.preventDefault()
      let values = getFormValues(el)
      values = parseFormValues(values)
      values.require_ids =
        (values.require_ids && values.require_ids.map(rmap => rmap.id)) || []
      const errors = getTasks().validateForm(values, unitSchema, [
        'name',
        'language',
        'body',
        'require_ids',
      ])
      if (errors && errors.length) {
        return
      }
      getTasks().addMemberToAddUnits(values)
      getTasks().route('/create/unit/list')
    },

    'submit .create--subject-add__form'(e, el) {
      if (e) e.preventDefault()
      const q = el.querySelector('input').value
      getTasks().search({ q, kind: 'unit,subject' })
    },

    'submit .create--unit-add__form'(e, el) {
      if (e) e.preventDefault()
      const q = el.querySelector('input').value
      getTasks().search({ q, kind: 'unit' })
    },

    'click .create--subject-add__add'(e, el) {
      if (e) e.preventDefault()
      const { kind, id, name, body } = el.dataset
      getTasks().addMemberToCreateSubject({ kind, id, name, body })
    },

    'click .create--unit-add__add'(e, el) {
      if (e) e.preventDefault()
      const { id, name, body, version } = el.dataset
      getTasks().addMemberToAddUnits({ id, name, body, version })
    },

    'click .create--subject-create .form-field--entities__a'(e, el) {
      if (e) e.preventDefault()
      const form = closest(el, 'form')
      const values = getFormValues(form)
      getTasks().createSubjectData(values)
      getTasks().route('/create/subject/add')
    },

    'click .create--unit-create .form-field--entities__a'(e, el) {
      if (e) e.preventDefault()
      const form = closest(el, 'form')
      let values = getFormValues(form)
      values = parseFormValues(values)
      getTasks().stowProposedUnit(values)
      getTasks().route('/create/unit/create/add')
    },

    'click .create--subject-create .form-field--entities__remove'(e, el) {
      if (e) e.preventDefault()
      const { id } = el
      getTasks().removeMemberFromCreateSubject({ id })
    },

    'click .create--unit-find__choose'(e, el) {
      if (e) e.preventDefault()
      const { id, name } = el.dataset
      getTasks().createChooseSubjectForUnits({ id, name })
    },

    'submit .create--unit-find__form'(e, el) {
      if (e) e.preventDefault()
      const q = el.querySelector('input').value
      getTasks().search({ q, kind: 'subject' })
    },

    'click .create--card-find__choose'(e, el) {
      if (e) e.preventDefault()
      const { id, name } = el.dataset
      getTasks().createChooseUnitForCards({ id, name })
    },

    'submit .create--card-find__form'(e, el) {
      if (e) e.preventDefault()
      const q = el.querySelector('input').value
      getTasks().search({ q, kind: 'unit' })
    },

    'submit .create--unit-create-add__form'(e, el) {
      if (e) e.preventDefault()
      const q = el.querySelector('input').value
      getTasks().search({ q, kind: 'unit' })
    },

    'click .create--unit-create-add__add'(e, el) {
      if (e) e.preventDefault()
      const { id, name, body } = el.dataset
      getTasks().addRequireToProposedUnit({ id, name, body, kind: 'unit' })
    },

    'click .create--unit-list__remove'(e, el) {
      if (e) e.preventDefault()
      const { index } = el.dataset
      getTasks().removeUnitFromSubject({ index })
    },

    'click .create--unit-list__submit'(e) {
      if (e) e.preventDefault()
      getTasks().createUnitsProposal()
    },

    'click .create--card-list__remove'(e, el) {
      if (e) e.preventDefault()
      const { index } = el.dataset
      getTasks().removeCardFromUnit({ index })
    },

    'click .create--card-list__submit'(e) {
      if (e) e.preventDefault()
      getTasks().createCardsProposal()
    },

    'change .create--card-create [name="kind"]'(e, el) {
      const form = closest(el, 'form')
      const values = getFormValues(form)
      getTasks().stowProposedCard(values)
    },

    'submit .create--card-create form'(e, el) {
      if (e) e.preventDefault()
      let values = getFormValues(el)
      values = parseFormValues(values)
      const errors = getTasks().validateForm(values, cardSchema, [
        'name',
        'language',
        'kind',
      ])
      if (errors && errors.length) {
        return
      }
      getTasks().addMemberToAddCards(values)
      getTasks().route('/create/card/list')
    },
  })
}



const wizard = require('../components/wizard.tmpl')

module.exports = {
  unitWizard(state = 'find') {
    return wizard({
      options: [
        {
          label: 'Find Subject',
          name: 'find',
        },
        {
          label: 'Add Units',
          name: 'list',
        },
        {
          label: 'View',
          name: 'view',
        },
      ],
      state,
    })
  },

  cardWizard(state = 'find') {
    return wizard({
      options: [
        {
          label: 'Find Unit',
          name: 'find',
        },
        {
          label: 'Add Cards',
          name: 'list',
        },
        {
          label: 'View',
          name: 'view',
        },
      ],
      state,
    })
  },
}


*/
