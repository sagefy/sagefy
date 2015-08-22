{div, h1, p, br, a, i} = require('../../modules/tags')

module.exports = ->
    return div(
        {id: 'log-in', className: 'col-6'}
        h1('Log In')
        p(
            'Don\'t have an account? '
            a(
                {href: '/sign_up'}
                i({className: 'fa fa-user'})
                ' Sign Up'
            )
            '.'
            br()
            'Forgot your password? '
            a(
                {href: '/password'}
                i({className: 'fa fa-refresh'})
                ' Reset'
            )
            '.'
        )
    )
