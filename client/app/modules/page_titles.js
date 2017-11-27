const routes = [
  {
    path: '/sign_up',
    title: 'Sign Up',
  },
  {
    path: '/log_in',
    title: 'Log In',
  },
  {
    path: '/password',
    title: 'Password',
  },
  {
    path: '/styleguide',
    title: 'Styleguide',
  },
  {
    path: '/terms',
    title: 'Privacy & Terms',
  },
  {
    path: '/contact',
    title: 'Contact',
  },
  {
    path: '/settings',
    title: 'Settings',
  },
  {
    path: '/notices',
    title: 'Notices',
  },
  {
    path: '/search',
    title: 'Search',
  },
  {
    path: '/create/subject/create',
    title: 'Create a New Subject',
  },
  {
    path: '/create/subject/add',
    title: 'Add Existing Members to a Subject',
  },
  {
    path: '/create/unit/find',
    title: 'Find a Subject to Add Units',
  },
  {
    path: '/create/unit/list',
    title: 'Add Units to Subject',
  },
  {
    path: '/create/unit/add',
    title: 'Add Existing Unit to Subject',
  },
  {
    path: '/create/unit/create/add',
    title: 'Find Requires for New Unit',
  },
  {
    path: '/create/unit/create',
    title: 'Create a New Unit for Subject',
  },
  {
    path: '/create/card/find',
    title: 'Find a Unit to Add Cards',
  },
  {
    path: '/create/card/list',
    title: 'Add Cards to Unit',
  },
  {
    path: '/create/card/create',
    title: 'Create a New Card for Unit',
  },
  {
    path: '/create',
    title: 'Create',
  },
  {
    path: /^\/topics\/(create|[\d\w\-_]+\/update)$/,
    title: 'Topic',
    // Must be before `topic`
  },
  {
    path: '/topics/{id}/posts/create',
    title: 'Create Post',
  },
  {
    path: '/topics/{id}/posts/{id}/update',
    title: 'Update Post',
  },
  {
    path: '/topics/{id}',
    title: 'Topic',
  },
  {
    path: '/users/{id}',
    title: 'Profile',
  },
  {
    path: '/cards/{id}',
    title: 'Card',
  },
  {
    path: '/units/{id}',
    title: 'Unit',
  },
  {
    path: '/subjects/{id}',
    title: 'Subject',
  },
  {
    path: /^\/(card|unit|subject)s\/([\w\d-]+)\/versions$/,
    title: 'Versions',
  },
  {
    path: '/follows',
    title: 'Follows',
  },
  {
    path: '/recommended_subjects',
    title: 'Recommended Subjects',
  },
  {
    path: '/my_subjects',
    title: 'My Subjects',
  },
  {
    path: '/subjects/{id}/tree',
    title: 'Subject Tree',
  },
  {
    path: '/subjects/{id}/choose_unit',
    title: 'Choose Unit',
  },
  {
    path: '/cards/{id}/learn',
    title: 'Learn',
  },
  {
    path: '/subjects/{id}/landing',
    title: 'An Introduction to Electronic Music',
  },
  {
    path: /^\/suggest.*$/,
    title: 'Suggest free online learning experiences',
  },
  {
    path: /^\/?$/,
    title: 'Home',
    // Must be 2nd to last
  },
  {
    path: /.*/,
    title: '404',
    // Must be last
  },
]

module.exports = routes
