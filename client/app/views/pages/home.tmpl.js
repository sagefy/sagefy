// TODO-3 move copy to content directory
const {div, img, hgroup, h1, h3, p, a} = require('../../modules/tags')
const icon = require('../components/icon.tmpl')

module.exports = (data) => {
    return (
        div(
            {id: 'home'},
            img(
                {src: '/astrolabe.svg', className: 'home__logo'}
            ),
            hgroup(
                h1('Sagefy'),
                h3('Open-content adaptive learning platform.')
            ),
            data.currentUserID ? p(
                'Logged in. ',
                a(
                    {href: '/my_sets'},
                    'My Sets ',
                    icon('next')
                )
            ) : null,
            data.currentUserID ? null : p(
                a({href: '/log_in'}, icon('log-in'), ' Log In'),
                ' or ',
                a({href: '/sign_up'}, icon('sign-up'), ' Sign Up')
            ),
            p(
                'What is Sagefy? ',
                a(
                    {href: 'https://www.youtube.com/watch?v=HVwfwTOdnOE'},
                    'Watch this 3 minute YouTube video'
                ),
                '.'
            ),
            p(
                {className: 'alert--accent'},
                'Sagefy is very new. You will likely find bugs ',
                'and other strange behaviors, as well as a general lack of ',
                'content. Please report issues ',
                'to <support@sagefy.org>. Thank you!'
            ),  // TODO-2 Delete this warning message
            p(
                {className: 'home__legal'},
                '© Copyright 2016 Sagefy. ',
                a({href: '/terms'}, icon('terms'), ' Privacy & Terms'),
                '.'
            )
        )
    )
}
