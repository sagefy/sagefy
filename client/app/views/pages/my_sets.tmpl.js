const {div, h1, ul, li, h3, p, button, a} = require('../../modules/tags')
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
        {id: 'my-sets'},
        h1('My Sets'),
        ul(data.userSets.map(set => userSet(set))),
        data.userSets.length === 0 ? p(
            a(
                {href: '/search?mode=as_learner'},
                icon('search'),
                ' Find a set'
            ),
            ' to get started.'
        ) : p(
            a(
                {href: '/search?mode=as_learner'},
                icon('search'),
                ' Find another set'
            )
        )
    )
}

const userSet = (data) =>
    li(
        {className: 'my-set'},
        button(
            {
                className: 'engage-set',
                id: data.entity_id
            },
            icon('good'),
            ' Engage'
        ),
        div(
            {className: 'my-set-right'},
            h3(data.name),
            p(data.body),
            a(
                {href: `/sets/${data.entity_id}/tree`},
                icon('unit'),
                ' View Units'
            )
        )
    )
