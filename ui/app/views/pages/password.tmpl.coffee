{div, h1, nav, ol, li, a} = require('../../modules/tags')

module.exports = ->
    return div(
        {id: 'password', className: 'col-8'}
        h1('Create a New Password')
        ol(
            {className: 'wizard'}
            li(
                {href: '#', className: 'email selected'}
                'Enter Email'
            )
            li(
                {href: '#', className: 'inbox'}
                'Check Inbox'
            )
            li(
                {href: '#', className: 'password'}
                'Change Password'
            )
        )
    )
