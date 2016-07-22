# TODO-3 move copy to content directory
{div, img, hgroup, h1, h3, p, a, i} = require('../../modules/tags')
icon = require('../components/icon.tmpl')

module.exports = (data) ->
    return (
        div(
            {id: 'home'}
            img(
                {src: '/astrolabe.svg', className: 'home__logo'}
            )
            hgroup(
                h1('Sagefy')
                h3(
                    'Open-content adaptive learning platform.'
                )
            )
            p(
                'Logged in. '
                a(
                    {href: '/my_sets'}
                    'My Sets '
                    icon('next')
                )
            ) if data.currentUserID
            p(
                a({href: '/log_in'}, icon('log-in'), ' Log In')
                ' or '
                a({href: '/sign_up'}, icon('sign-up'), ' Sign Up')
            ) unless data.currentUserID
            p(
                'What is Sagefy? '
                a(
                    {href: 'https://www.youtube.com/watch?v=HVwfwTOdnOE'}
                    'Watch this 3 minute YouTube video'
                )
                '.'
            )
            p(
                {className: 'alert--accent'}
                '''
                Sagefy is very new. You will likely find bugs
                and other strange behaviors, as well as a general lack of
                content. Please help by creating content and reporting issues
                to <support@sagefy.org>. Thank you!
                '''
            ) # TODO-2 Delete this warning message
            p(
                {className: 'home__legal'}
                '© Copyright 2015 Sagefy. '
                a({href: '/terms'}, icon('terms'), ' Privacy & Terms')
                '.'
            )
        )
    )
