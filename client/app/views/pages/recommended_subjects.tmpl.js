const { div, h1, ul, li, a, hr } = require('../../modules/tags')
const icon = require('../components/icon.tmpl')
const spinner = require('../components/spinner.tmpl')
const previewSubjectHead = require('../components/preview_subject_head.tmpl')

const subjectResult = subject =>
    [
        a(  // TODO-2 if already in subjects, don't show this button
            {
                id: subject.entity_id,
                href: '#',
                className: 'add-to-my-subjects',
            },
            icon('create'),
            ' Add to My Subjects'
        ),
        div(
            { className: 'recommended-subjects__right' },
            previewSubjectHead({ name: subject.name, body: subject.body }),
            a(
                {
                    href: `/subjects/${subject.entity_id}/tree`,
                    className: 'recommended-subjects__view-units',
                },
                icon('unit'),
                ' View Units'
            )
        ),
    ]


module.exports = (data) => {
    if(!data.recommendedSubjects.length) { return spinner() }
    return div(
        { id: 'recommended-subjects', className: 'page' },
        h1('Recommended Subjects'),
        ul(
            data.recommendedSubjects.map(subject => li(subjectResult(subject)))
        ),
        hr(),
        a({ href: '/search?mode=as_learner' }, icon('search'), ' Search Subjects')
    )
}
