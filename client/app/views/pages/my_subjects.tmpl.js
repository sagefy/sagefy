const { div, h1, ul, li, p, button, a, br } = require('../../modules/tags')
// const c = require('../../modules/content').get
const spinner = require('../components/spinner.tmpl')
const icon = require('../components/icon.tmpl')
const info = require('../components/entity_info.tmpl')
const previewSubjectHead = require('../components/preview_subject_head.tmpl')

module.exports = (data) => {
  if (!data.userSubjects) {
    return spinner()
  }

  return div(
    { id: 'my-subjects', className: 'page' },
    h1('My Subjects'),
    p(
      { className: 'alert--accent' },
      icon('follow'),
      ' Sagefy is new. You will likely find bugs. ',
      br(),
      'Please report issues to <support@sagefy.org>. ',
      'Thank you!'
    ), // TODO-2 Delete this warning message
    ul(
      { className: 'my-subjects__list' },
      data.userSubjects.map(subject => userSubject(subject))
    ),
    data.userSubjects.length === 0
      ? p(
          a(
            // TODO-2 temporary {href: '/search?mode=as_learner'},
            {
              href: '/recommended_subjects',
              className: 'my-subjects__find-first-subject',
            },
            icon('search'),
            ' See Recommended Subjects'
          ),
          ' to get started.'
        )
      : p(
          a(
            // TODO-2 temporary {href: '/search?mode=as_learner'},
            { href: '/recommended_subjects' },
            icon('search'),
            ' Find another subject'
          )
        ),
    info()
  )
}

const userSubject = data =>
  li(
    { className: 'my-subject' },
    button(
      {
        className: 'my-subjects__engage-subject',
        id: data.entity_id,
      },
      'Engage ',
      icon('next')
    ),
    div(
      { className: 'my-subjects__my-subject-right' },
      previewSubjectHead({ name: data.name, body: data.body })
    )
  )
