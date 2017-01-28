/* eslint-disable */

// TODO-3 move copy to content directory
const {div, header, img, hgroup, h1, h2, h3, h4, h5, h6, p, a, hr, strong, ul, ol, li, iframe, br, footer} = require('../../modules/tags')
const icon = require('../components/icon.tmpl')

// TODO-1 Include unique CTAs throughout

module.exports = data => {
    const cta = a({href: '/sign_up', className: 'home__cta-button'}, icon('sign-up'), ' Sign Up');

    return div(
        {id: 'home', className: 'page'},
        header(
          img(
              {src: '/astrolabe.svg', className: 'home__logo'}
          ),
          hgroup(
              h1('Sagefy'),
              h3('Learn anything, customized for you.'),
              h6('And always free.')
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
          )
        ),
        hr(),
        data.currentUserID ? null : div(
          hgroup(
            h2('What is Sagefy?'),
            h5('Sagefy is an open-content adaptive learning platform.')
          ),
          p(
            strong('Adaptive Learning.'),
            ' Get the most out of your time and effort spent. Sagefy optimizes the learning experience based on what you already know and what your goal is. Sagefy presents small pieces of content based on your responses.'
          ),
          p(
            strong('Open-Content.'),
            ' Anyone can view, share, create, and edit content. Open-content means that Sagefy reaches a range of learning subjects.'
          ),
          h2('Why learn with Sagefy?'),
          ul(
            li('Learn any subject'),
            li('Create and edit any content'),
            li('Skip what you already know'),
            li('Build up to where you need to be'),
            li('Choose your own path'),
            li('Discussion built in')
          ),
          cta,
          h2('How do I learn with Sagefy?'),
          ol(
            li('Create an account'),
            li('Find and add a set'),
            li('Choose your unit'),
            li('Learn')
          ),
          iframe({
            width: "560",
            height: "315",
            src: "https://www.youtube.com/embed/HVwfwTOdnOE",
            frameborder: "0",
            allowfullscreen: true
          }),
          p(
            'Also check out the in-detail ',
            a({href: 'https://stories.sagefy.org/why-im-building-sagefy-731eb0ceceea'}, 'article on Medium'),
            '.'
          ),
          cta,
          h2('Popular Sets'),
          ul(
            li(
              a({href: 'https://sagefy.org/sets/CgDRJPfzJuTR916HdmosA3A8'}, 'An Introduction to Electronic Music - Foundation'),
              br(),
              'A small taste of the basics of electronic music. These units serve as the basis for topics on creating and changing sound.'
            )
          ),
          cta,
          // TODO-1 third party validation
          h2('Features'),
          ul(
            li('Simple organization. The only kinds of things are sets (courses), units (a learning goal), and cards (a small learning experience).'),
            li('Choose your path along the way. Sagefy recommends, but never requires.'),
            li('Keep up to speed with review reminders.'),
            li('Variety of types of cards, so you can stay motivated.'),
            li('Focus on what you want to learn with no distractions.'),
            li('Skip content you already know.'),
            li('Really learn it, instead of skimming the top.')
          ),
          cta,
          h2('Comparison'),
          ul(
            li(
              strong('Classroom'),
              ': Difficult to adapt, expensive.'
            ),
            li(
              strong('Learning Management Systems'),
              ': Online, but still difficult to adapt, often expensive.'
            ),
            li(
              strong('Closed Adaptive Systems'),
              ': Limited range of topics.'
            ),
            li(
              strong('Massive Online Courses'),
              ': Rarely adapts. Set time frame.'
            ),
            li(
              strong('Flash Cards'),
              ': Limited depth of practice.'
            )
          ),
          cta,
          hr()
        ),
        footer(
          ul(
            li(a({href: 'https://docs.sagefy.org/'}, 'Docs')),
            li(a({href: 'https://stories.sagefy.org/'}, 'Stories (Blog)')),
            li(a({href: 'https://sagefy.uservoice.com/forums/233394-general/'}, 'Support'))
          ),
          p(
              {className: 'home__legal'},
              '© Copyright 2016 Sagefy. ',
              a({href: '/terms'}, icon('terms'), ' Privacy & Terms'),
              '.'
          )
        )
    )
};
