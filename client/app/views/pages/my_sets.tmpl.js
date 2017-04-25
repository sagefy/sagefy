const {div, h1, ul, li, p, button, a, br} =
    require('../../modules/tags')
// const c = require('../../modules/content').get
const spinner = require('../components/spinner.tmpl')
const icon = require('../components/icon.tmpl')
const info = require('../components/entity_info.tmpl')
const previewSetHead = require('../components/preview_set_head.tmpl')

module.exports = (data) => {
    if(!data.userSets) { return spinner() }

    return div(
        {id: 'my-sets', className: 'page'},
        h1('My Sets'),
        p(
            {className: 'alert--accent'},
            icon('follow'),
            ' Sagefy is new. You will likely find bugs. ',
            br(),
            'Please report issues to <support@sagefy.org>. ',
            'Thank you!'
        ),  // TODO-2 Delete this warning message
        ul(
          {className: 'my-sets__list'},
          data.userSets.map(set => userSet(set))
        ),
        data.userSets.length === 0 ? p(
            a(
                // TODO-2 temporary {href: '/search?mode=as_learner'},
                {
                    href: '/recommended_sets',
                    className: 'my-sets__find-first-set',
                },
                icon('search'),
                ' See Recommended Sets'
            ),
            ' to get started.'
        ) : p(
            a(
                // TODO-2 temporary {href: '/search?mode=as_learner'},
                {href: '/recommended_sets'},
                icon('search'),
                ' Find another set'
            )
        ),
        info()
    )
}

const userSet = (data) =>
    li(
        {className: 'my-set'},
        button(
            {
                className: 'my-sets__engage-set',
                id: data.entity_id
            },
            'Engage ',
            icon('next')
        ),
        div(
            {className: 'my-sets__my-set-right'},
            previewSetHead({ name: data.name, body: data.body })
        )
    )
