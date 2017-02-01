/* eslint-disable */

// TODO-3 move copy to content directory
const {div, header, img, hgroup, h1, h2, h3, h4, h5, h6, p, a, hr, strong, ul, ol, li, iframe, br, footer, span, em, section} = require('../../modules/tags')
const icon = require('../components/icon.tmpl')

// TODO-1 Include unique CTAs throughout

module.exports = data => {
    const cta = a({href: '/sign_up', className: 'home__cta-button'}, icon('sign-up'), ' Sign Up')

    const w = (n) => span({className: 'home__icon-wrap'}, n)

    return div(
        {id: 'home', className: 'page'},
        header(
          img(
              {src: '/astrolabe.svg', className: 'home__logo'}
          ),
          hgroup(
              h1('Sagefy'),
              h3('Learn anything, customized for you.'),
              h6('...and always free.')
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
        data.currentUserID ? null : div(
          section(
            hgroup(
              h2('What is Sagefy?'),
              h5('Sagefy is an open-content adaptive learning platform.')
            ),
            p(
              strong('Adaptive Learning.'),
              ' Get the most out of your time and effort spent. Sagefy optimizes based on what you already know and what your goal is.'
            ),
            p(
              strong('Open-Content.'),
              ' Anyone can view, share, create, and edit content. Open-content means that Sagefy reaches a range of learning subjects.'
            ),
            cta
          ),
          section(
            h2('Why learn with Sagefy?'),
            ul(
              {className: 'home__ul--why'},
              li(w(icon('learn')), em(' Learn any subject.')),
              li(w(icon('create')), em(' Create and edit any content.')),
              li(w(icon('fast')), em(' Skip what you already know.')),
              li(w(icon('grow')), em(' Build up to where you need to be.')),
              li(w(icon('search')), em(' Choose your own path.')),
              li(w(icon('topic')), em(' Discussion built in.'))
            ),
            cta
          ),
          section(
            h2('How do I learn with Sagefy?'),
            ol(
              {className: 'home__ul--how'},
              li(img({src: 'https://i.imgur.com/qrPmvzZ.png'}), 'Create an account.'),
              li(img({src: 'https://i.imgur.com/9KJdaFl.png'}), 'Find and add a set.'),
              li(img({src: 'https://i.imgur.com/uLJstC1.png'}), 'Choose your unit.'),
              li(img({src: 'https://i.imgur.com/BlUMbif.png'}), 'Learn.')
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
            cta
          ),
          section(
            h2('Popular Sets'),
            ul(
              li(
                a({href: 'https://sagefy.org/sets/CgDRJPfzJuTR916HdmosA3A8/landing'}, 'An Introduction to Electronic Music - Foundation'),
                br(),
                'A small taste of the basics of electronic music. These units serve as the basis for topics on creating and changing sound.'
              )
            ),
            cta
          ),
          // TODO-1 third party validation
          section(
            h2('Features'),
            ul(
              {className: 'home__ul--features'},
              li(w(icon('unit')), strong('Simple'), ' organization. The only kinds of things are: ',
                ul(
                  li('Sets -- or courses,'),
                  li('Units -- or learning goals, and'),
                  li('Cards -- small learning experiences.')
                )
              ),
              li(w(icon('search')), strong('Choose'), ' your path along the way. Sagefy recommends, but never requires.'),
              li(w(icon('reply')), 'Keep up to speed with ', strong('review'), ' reminders.'),
              li(w(icon('follow')), strong('Variety'), ' of types of cards, so you can stay motivated.'),
              li(w(icon('good')), 'Focus on what you want to learn with ', strong('no distractions.')),
              li(w(icon('fast')), strong('Skip'), ' content you already know.'),
              li(w(icon('learn')), 'Learn ', strong('deeply'), ', instead of skimming the top.')
            ),
            cta
          ),
          section(
            h2('Comparison'),
            ul(
              li(
                strong('Classroom'),
                ': When we adapt the content to what you already know, we keep the motivation going and reduce effort and time. Classrooms are a difficult place to get personal. Sagefy optimizes for what you already know, every time.'
              ),
              li(
                strong('Learning Management Systems'),
                ': Great cost and time savings come from using technology. LMSs are designed to support the classroom model. With Sagefy, you get both the benefits of online learning and a highly personalized experience.'
              ),
              li(
                strong('Closed Adaptive Systems'),
                ': You should be able to pursue your own goals. Closed systems means only select topics are available. An open-content system like Sagefy reaches a range of topics.'
              ),
              li(
                strong('Massive Online Courses'),
                ': MOOCs reach a large range, but offer little adaption and only support expert-created content. Sagefy has no deadlines -- learn when you see fit.'
              ),
              li(
                strong('Flash Cards'),
                ': Flash cards are great for memorizing content. But what about integration and application of knowledge? Sagefy goes deeper than flash cards.'
              )
            ),
            cta
          )
        ),
        footer(
          ul(
            li('© Copyright 2017 Sagefy.'),
            li(a({href: 'https://docs.sagefy.org/'}, 'Docs')),
            li(a({href: 'https://stories.sagefy.org/'}, 'Stories (Blog)')),
            li(a({href: 'https://sagefy.uservoice.com/forums/233394-general/'}, icon('contact'), ' Support')),
            li(a({href: '/terms'}, icon('terms'), ' Privacy & Terms'))
          )
        )
    )
};
