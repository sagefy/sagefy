const {
  field,
  collection,
  // isRequired,
} = require('redux-schemad')

/*
const card = 'card'
const unit = 'unit'
const subject = 'subject'
const entityKinds = [card, unit, subject]

const post = 'post'
const proposal = 'proposal'
const vote = 'vote'
const postKinds = [post, proposal, vote]

const topic = 'topic'
const followKinds = entityKinds.concat(topic)

const pending = 'pending'
const blocked = 'blocked'
const declined = 'declined'
const accepted = 'accepted'
const entityStatues = [pending, blocked, declined, accepted]

const video = 'video'
const page = 'page'
const unscoredEmbed = 'unscored_embed'
const choice = 'choice'
const cardKinds = [video, page, unscoredEmbed, choice]
*/

const stateSchema = {
  haveCheckedSession: field(),
  isMenuOpen: field(),
  currentUserId: field(),
  currentSubjectId: field(),
  currentUnitId: field(),
  currentCardId: field(),
  recommendedSubjects: field(), // array of ids
  routePath: field(),
  routeQuery: field(),
  routeTitle: field(),
  nextMethod: field(),
  nextPath: field(),
  users: collection('id', {
    id: field(),
    created: field(),
    modified: field(),
    name: field(),
    email: field(),
    settings: field(),
    avatar: field(),
  }),
  topics: collection('id', {
    id: field(),
    created: field(),
    modified: field(),
    userId: field(),
    name: field(),
    entityId: field(),
    entityKind: field(),
  }),
  posts: collection('id', {
    id: field(),
    created: field(),
    modified: field(),
    userId: field(),
    topicId: field(),
    kind: field(),
    body: field(),
    repliesToId: field(),
    entityVersions: field(),
    response: field(),
  }),
  notices: collection('id', {
    id: field(),
    created: field(),
    modified: field(),
    userId: field(),
    kind: field(),
    data: field(),
    read: field(),
    tags: field(),
  }),
  follows: collection('id', {
    id: field(),
    created: field(),
    modified: field(),
    userId: field(),
    entityId: field(),
    entityKind: field(),
  }),
  usersSubjects: collection('id', {
    id: field(),
    created: field(),
    modified: field(),
    userId: field(),
    subjectId: field(),
  }),
  responses: collection('id', {
    id: field(),
    created: field(),
    modified: field(),
    userId: field(),
    cardId: field(),
    unitId: field(),
    response: field(),
    score: field(),
    learned: field(),
  }),
  units: collection('versionId', {
    versionId: field(),
    created: field(),
    modified: field(),
    entityId: field(),
    previousId: field(),
    language: field(),
    name: field(),
    status: field(),
    available: field(),
    tags: field(),
    userId: field(),
    body: field(),
    requireIds: field(),
  }),
  subjects: collection('versionId', {
    versionId: field(),
    created: field(),
    modified: field(),
    entityId: field(),
    previousId: field(),
    language: field(),
    name: field(),
    status: field(),
    available: field(),
    tags: field(),
    userId: field(),
    body: field(),
    members: field(),
  }),
  cards: collection('versionId', {
    versionId: field(),
    created: field(),
    modified: field(),
    entityId: field(),
    previousId: field(),
    language: field(),
    name: field(),
    status: field(),
    available: field(),
    tags: field(),
    userId: field(),
    unitId: field(),
    requireIds: field(),
    kind: field(),
    data: field(),
  }),
  searchResults: collection('id', {
    id: field(),
    // ???
  }),
  searchResultsOrder: field(), // array of ids. necessary?
  errors: collection('id', {
    id: field(),
    // ???
  }),
  networkRequests: collection('id', {
    id: field(),
    endpoint: field(),
    status: field(),
    // ???
  }),
  forms: collection('name', {
    name: field(),
    data: field(),
  }),
  //
  create$kind: field(), // the kind of things we'll create
  create$step: field(),
  create$recentSubjects: field(), // array of ids
  create$recentUnits: field(), // array of ids
  create$selectedId: field(), // what we've selected to add to
  create$selectedKind: field(),
  create$subjects: collection(),
  create$units: collection(),
  create$cards: collection(),
}

module.exports = { stateSchema }
