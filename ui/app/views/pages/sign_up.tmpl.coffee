{div, h1, p, a, i, br} = require('../../modules/tags')

module.exports = ->
    return div(
        {id: 'sign-up', className: 'col-6'}
        h1('Sign Up')
        p(
            'Already have an account? '
            a(
                {href: '/log_in'}
                i({className: 'fa fa-sign-in'})
                ' Log In'
            )
            '.'
            br()
            'By signing up, you agree to our '
            a(
                {href: '/terms'}
                ' Terms of Service'
            )
            '.'
        )
    )
