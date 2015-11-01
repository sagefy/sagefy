{div, h1, ul, li, h3, p, button, a} = require('../../modules/tags')
c = require('../../modules/content').get

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
    return div(
        {id: 'my-sets', className: 'col-10'}
        h1('My Sets')
        div({className: 'spinner'}) unless data.userSets
        ul(userSet(set) for set in data.userSets) if data.userSets
    )

userSet = (data) ->
    return li(
        {className: 'my-set'}
        button(
            {
                className: 'engage-set'
                id: data.entity_id
            }
            'Engage!'
        )
        div(
            {className: 'my-set-right'}
            h3(data.name)
            p(data.body)
            a(
                {href: "/set/#{data.entity_id}/tree"}
                'View Units'
            )
        )
    )
