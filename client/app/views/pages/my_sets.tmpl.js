const {div, h1, ul, li, h3, p, button, a,
       strong, small, br} = require('../../modules/tags')
// const c = require('../../modules/content').get
const spinner = require('../components/spinner.tmpl')
const icon = require('../components/icon.tmpl')

/*
r.db('sagefy').table('users_sets').insert([{
  'user_id': 'thOCi8QoDUJyhJPYy63EY9Ml',
  'set_ids': ['a'],
}]);

  r.db('sagefy').table('sets').insert([{
    'created': r.now(),
    'modified': r.now(),
    'entity_id': 'a',
    'body': 'foo',
    'name': 'A grand set A.',
    'status': 'accepted',
    'members': [{
      'id': 'b',
      'kind': 'unit'
    }]
  }])
*/

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

const info = () =>
  div(
    {className: 'my-sets__info'},
    h3('What are cards, units, and sets?'),
    ul(
      li(
        'A ', strong('card'), ' is a single learning activity.',
        br(),
        small('(Examples: a 3-minute video or a multiple choice question.)')
      ),
      li(
        'A ', strong('unit'), ' is a single learning goal.',
        br(), small('(Example: "What is mean, median, and mode?")')
      ),
      li(
        'A ', strong('set'), ' is a collection of units and other sets.',
        br(),
        small(
          '(Like a course, but at any scale. ',
          'Such as "Measures of Central Tendency", "Intro to Statistics", ',
          'or even a full degree program.)'
        )
      )
    ),
    p(
      'For more details and examples, ',
      a(
        {href: 'https://youtu.be/HVwfwTOdnOE'},
        'check out this 3-minute overview video'
      ),
      '.'
    )
  )

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
            h3(data.name),
            p(data.body)
        )
    )
