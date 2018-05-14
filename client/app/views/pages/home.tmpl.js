// TODO-3 move copy to content directory
const {
  div,
  header,
  img,
  hgroup,
  h1,
  h2,
  h3,
  h5,
  h6,
  p,
  a,
  strong,
  ul,
  ol,
  li,
  iframe,
  footer,
  span,
  section,
} = require('../../modules/tags')
const icon = require('../components/icon.tmpl')
const spinner = require('../components/spinner.tmpl')
const previewSubjectHead = require('../components/preview_subject_head.tmpl')
const { getIsLoggedIn } = require('../../selectors/base')

// TODO-1 Include unique CTAs throughout

module.exports = data => {
  if (getIsLoggedIn(data) === null) {
    return spinner()
  }

  const cta = a(
    { href: '/sign_up', className: 'home__cta-button' },
    icon('sign-up'),
    ' Sign Up'
  )

  const w = n => span({ className: 'home__icon-wrap' }, n)

  return div(
    { id: 'home', className: 'page' },
    header(
      img({ src: '/astrolabe.svg', className: 'home__logo' }),
      hgroup(
        h1('Sagefy'),
        h3('Learn anything, customized for you.'),
        h6('...and always free.')
      ),
      getIsLoggedIn(data)
        ? p(
            'Logged in. ',
            a({ href: '/my_subjects' }, 'My Subjects ', icon('next'))
          )
        : p(
            a({ href: '/log_in' }, icon('log-in'), ' Log In'),
            ' or ',
            a({ href: '/sign_up' }, icon('sign-up'), ' Sign Up')
          )
    ),
    getIsLoggedIn(data)
      ? null
      : div(
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
            h2('How do I learn with Sagefy?'),
            ol(
              { className: 'home__ul--how' },
              li(
                img({ src: 'https://i.imgur.com/2QSMPNs.png' }),
                'Create an account.'
              ),
              li(
                img({ src: 'https://i.imgur.com/xKRaoff.png' }),
                'Find and add a subject.'
              ),
              li(
                img({ src: 'https://i.imgur.com/MYTGawz.png' }),
                'Choose your unit.'
              ),
              li(img({ src: 'https://i.imgur.com/yjeVPiq.png' }), 'Learn.')
            ),
            cta
          ),
          section(
            h2('Popular Subjects'),
            ul(
              { className: 'home__ul--popular-subjects' },
              li(
                previewSubjectHead({
                  url: '/subjects/UIe3mx3UTQKHDG2zLyHI5w/landing',
                  name: 'An Introduction to Electronic Music',
                  body:
                    'A small taste of the basics of electronic music. Learn the concepts behind creating and modifying sounds in an electronic music system. Learn the ideas behind the tools and systems we use to create electronic music.',
                })
              )
            ),
            cta
          ),
          section(
            h2('Why learn with Sagefy?'),
            ul(
              { className: 'home__ul--why' },
              li(w(icon('learn')), span(strong('Learn'), ' any subject.')),
              li(
                w(icon('fast')),
                span(strong('Skip'), ' what you already know.')
              ),
              li(
                w(icon('grow')),
                span(strong('Build up'), ' to where you need to be.')
              ),
              li(w(icon('search')), span(strong('Choose'), ' your own path.')),
              li(
                w(icon('learn')),
                span(
                  'Learn ',
                  strong('deeply'),
                  ', instead of skimming the top.'
                )
              ),
              li(
                w(icon('follow')),
                span(
                  'Stay ',
                  strong('motiviated'),
                  ' with different types of cards.'
                )
              ),
              li(
                w(icon('good')),
                span(
                  'Focus on what you want to learn with ',
                  strong('no distractions.')
                )
              ),
              li(
                w(icon('create')),
                span('Create and edit ', strong('any'), ' content.')
              ),
              li(
                w(icon('topic')),
                span(strong('Discuss'), ' anything as you learn.')
              )
            ),
            cta
          ),
          section(
            h2('What does Sagefy provide?'),
            iframe({
              width: '560',
              height: '315',
              src: 'https://www.youtube.com/embed/gFn4Q9tx7Qs',
              frameborder: '0',
              allowfullscreen: true,
            }),
            p(
              'Also check out the in-detail ',
              a(
                {
                  href:
                    'https://stories.sagefy.org/why-im-building-sagefy-731eb0ceceea',
                },
                'article on Medium'
              ),
              '.'
            ),
            cta
          ),
          // TODO-1 third party validation

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
                ': Pursue your own goals. Closed systems means only select topics are available. An open-content system like Sagefy reaches a range of topics.'
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
        li('© Copyright 2018 Sagefy.'),
        li(a({ href: 'https://docs.sagefy.org/' }, 'Docs')),
        li(a({ href: 'https://stories.sagefy.org/' }, 'Stories (Blog)')),
        li(a({ href: 'https://sgef.cc/devupdates' }, 'Updates')),
        li(
          a(
            {
              href: 'https://sagefy.uservoice.com/forums/233394-general/',
            },
            icon('contact'),
            ' Support'
          )
        ),
        li(a({ href: '/terms' }, icon('terms'), ' Privacy & Terms'))
      )
    )
  )
}
