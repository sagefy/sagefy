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
                {style: {
                    background: 'rgb(255, 236, 239)'
                    color: 'rgb(197, 124, 139)'
                    borderRadius: '2px'
                    padding: '12px'
                }}
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
