// TODO-2 add `available` field
// TODO-2 on update: how to decline a proposal?
// TODO-3 Tags (all)

const { extend } = require('../../helpers/utilities')
const { prefixObjectKeys } = require('../../helpers/auxiliaries')

const postSchema = require('../../schemas/post')
const voteSchema = require('../../schemas/vote')
const proposalSchema = require('../../schemas/proposal')

const schemas = {
  post: postSchema,
  vote: voteSchema,
  proposal: proposalSchema,
}

const getFields = formData => {
  const fields = []
  ;['post.id', 'post.topic_id', 'post.replies_to_id'].forEach(name => {
    if (formData[name]) {
      fields.push({ name })
    }
  })

  /* PP@ fields.push({
    name: 'post.kind',
    options: [{
      label: 'Post',
      disabled: !!formData['post.id'],
    }, {
      label: 'Proposal',
      disabled: !!formData['post.id'],
    }, {
      label: 'Vote',
      disabled: !!formData['post.id'] ||
            !formData['post.replies_to_id']
    }],
    inline: true,
    label: 'Post Kind'
  }) */

  fields.push({
    name: 'post.kind',
    type: 'hidden',
  })

  if (formData['post.kind'] === 'vote') {
    fields.push({
      name: 'post.response',
      options: [{ label: 'Yes, I agree' }, { label: 'No, I dissent' }],
      inline: true,
      label: 'Response',
      disabled: !!formData['post.id'],
    })
  }

  fields.push({
    name: 'post.body',
    label:
      formData['post.kind'] === 'proposal' ? 'Proposal Summary' : 'Post Body',
    description:
      formData['post.kind'] === 'proposal'
        ? 'Describe the value of this proposal.'
        : null,
  })

  // TODO PP@ update proposal handling

  return fields
}

const getSchema = formData => {
  const schema = {}

  if (formData['post.kind'] === 'proposal') {
    extend(schema, prefixObjectKeys('post.', schemas.proposal))
  } else if (formData['post.kind'] === 'vote') {
    extend(schema, prefixObjectKeys('post.', schemas.vote))
  } else {
    extend(schema, prefixObjectKeys('post.', schemas.post))
  }

  return schema
}

module.exports = { getFields, getSchema }
