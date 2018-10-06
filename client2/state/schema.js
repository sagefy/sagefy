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

const schema = {
  haveCheckedSession: '',
  isMenuOpen: '',
  currentUserId: '',
  currentSubjectId: '',
  currentUnitId: '',
  currentCardId: '',
  recommendedSubjects: [], // array of ids
  routePath: '',
  routeQuery: '',
  routeTitle: '',
  nextMethod: '',
  nextPath: '',
  users: {
    '[id]': {
      created: '',
      modified: '',
      name: '',
      email: '',
      settings: '',
      avatar: '',
    },
  },
  topics: {
    '[id]': {
      created: '',
      modified: '',
      userId: '',
      name: '',
      entityId: '',
      entityKind: '',
    },
  },
  posts: {
    '[id]': {
      created: '',
      modified: '',
      userId: '',
      topicId: '',
      kind: '',
      body: '',
      repliesToId: '',
      entityVersions: '',
      response: '',
    },
  },
  notices: {
    '[id]': {
      created: '',
      modified: '',
      userId: '',
      kind: '',
      data: '',
      read: '',
      tags: '',
    },
  },
  follows: {
    '[id]': {
      created: '',
      modified: '',
      userId: '',
      entityId: '',
      entityKind: '',
    },
  },
  usersSubjects: {
    '[id]': {
      created: '',
      modified: '',
      userId: '',
      subjectId: '',
    },
  },
  responses: {
    '[id]': {
      created: '',
      modified: '',
      userId: '',
      cardId: '',
      unitId: '',
      response: '',
      score: '',
      learned: '',
    },
  },
  units: {
    '[versionId]': {
      created: '',
      modified: '',
      entityId: '',
      previousId: '',
      language: '',
      name: '',
      status: '',
      available: '',
      tags: '',
      userId: '',
      body: '',
      requireIds: '',
    },
  },
  subjects: {
    '[versionId]': {
      created: '',
      modified: '',
      entityId: '',
      previousId: '',
      language: '',
      name: '',
      status: '',
      available: '',
      tags: '',
      userId: '',
      body: '',
      members: '',
    },
  },
  cards: {
    '[versionId]': {
      created: '',
      modified: '',
      entityId: '',
      previousId: '',
      language: '',
      name: '',
      status: '',
      available: '',
      tags: '',
      userId: '',
      unitId: '',
      requireIds: '',
      kind: '',
      data: '',
    },
  },
  searchResults: {
    '[id]': {
      // ???
    },
  },
  searchResultsOrder: '', // array of ids. necessary?
  errors: {
    '[id]': {
      // ???
    },
  },
  networkRequests: {
    '[id]': {
      endpoint: '',
      status: '',
      // ???
    },
  },
  forms: {
    '[name]': {
      data: '',
    },
  },
  //
  create$kind: '', // the kind of things we'll create
  create$step: '',
  create$recentSubjects: '', // array of ids
  create$recentUnits: '', // array of ids
  create$selectedId: '', // what we've selected to add to
  create$selectedKind: '',
  create$subjects: {},
  create$units: {},
  create$cards: {},
}

module.exports = { schema }
