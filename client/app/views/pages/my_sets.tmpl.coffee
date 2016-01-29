{div, h1, ul, li, h3, p, button, a} = require('../../modules/tags')
c = require('../../modules/content').get
spinner = require('../components/spinner.tmpl')
icon = require('../components/icon.tmpl')

###
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
###

module.exports = (data) ->
    return spinner() unless data.userSets

    return div(
        {id: 'my-sets'}
        h1('My Sets')
        ul(userSet(set) for set in data.userSets)
        p(
            a(
                {href: '/search?mode=as_learner'}
                icon('search')
                ' Find a set'
            )
            ' to get started.'
        ) if data.userSets.length is 0
        p(
            a(
                {href: '/search?mode=as_learner'}
                icon('search')
                ' Find another set'
            )
        ) if data.userSets.length > 0
    )

userSet = (data) ->
    return li(
        {className: 'my-set'}
        button(
            {
                className: 'engage-set'
                id: data.entity_id
            }
            icon('good')
            ' Engage'
        )
        div(
            {className: 'my-set-right'}
            h3(data.name)
            p(data.body)
            a(
                {href: "/sets/#{data.entity_id}/tree"}
                icon('unit')
                ' View Units'
            )
        )
    )
