const Joi = require('joi')
const db = require('./index')

const postSchema = Joi.object().keys({
  id: Joi.string().guid(),
  created: Joi.date(),
  modified: Joi.date(),
  user_id: Joi.string().guid(),
  topic_id: Joi.string().guid(),
  kind: Joi.string().valid('post'),
  body: Joi.string(),
  replies_to_id: Joi.string().guid(),
})

const proposalSchema = postSchema.keys({
  kind: Joi.string().valid('proposal'),
  entity_versions: Joi.array()
    .items(
      Joi.object().keys({
        id: Joi.string().guid(),
        kind: Joi.string().valid('card', 'unit', 'subject'),
      })
    )
    .min(1),
})

const voteSchema = postSchema.keys({
  kind: Joi.string().valid('vote'),
  response: Joi.boolean(),
  body: Joi.string(),
  replies_to_id: Joi.string().guid(),
})

/*
insert_post
  query = """
    INSERT INTO posts
    (  user_id  ,   topic_id  ,   kind  ,   body  ,   replies_to_id  )
    VALUES
    (%(user_id)s, %(topic_id)s, %(kind)s, %(body)s, %(replies_to_id)s)
    RETURNING *;
  """

insert_proposal
  query = """
    INSERT INTO posts
    (  user_id  ,   topic_id  ,   kind  ,   body  ,
       replies_to_id  ,   entity_versions  )
    VALUES
    (%(user_id)s, %(topic_id)s, %(kind)s, %(body)s,
     %(replies_to_id)s, %(entity_versions)s)
    RETURNING *;
  """

insert_vote
  query = """
    INSERT INTO posts
    (  user_id  ,   topic_id  ,   kind  ,   body  ,
       replies_to_id  ,   response  )
    VALUES
    (%(user_id)s, %(topic_id)s, %(kind)s, %(body)s,
     %(replies_to_id)s, %(response)s)
    RETURNING *;
  """

update_post
  query = """
    UPDATE posts
    SET body = %(body)s
    WHERE id = %(id)s AND kind = 'post'
    RETURNING *;
  """

update_proposal
  query = """
    UPDATE posts
    SET body = %(body)s
    WHERE id = %(id)s AND kind = 'proposal'
    RETURNING *;
  """

update_vote
  query = """
    UPDATE posts
    SET body = %(body)s, response = %(response)s
    WHERE id = %(id)s AND kind = 'vote'
    RETURNING *;
  """

get_post
  query = """
    SELECT *
    FROM posts
    WHERE id = %(id)s
    LIMIT 1;
  """

list_posts_by_topic
  query = """
    SELECT *
    FROM posts
    WHERE topic_id = %(topic_id)s
    ORDER BY created ASC
    OFFSET %(offset)s
    LIMIT %(limit)s;
  """

list_posts_by_user
  query = """
    SELECT *
    FROM posts
    WHERE user_id = %(user_id)s
    ORDER BY created ASC;
  """

list_votes_by_proposal
  query = """
    SELECT *
    FROM posts
    WHERE kind = 'vote' AND replies_to_id = %(proposal_id)s
    ORDER BY created DESC;
  """
*/

async function getPost(postId) {}

async function listPostsByTopic(topicId) {}

async function listPostsByUser(userId) {}

async function listVotesByProposal(proposalId) {}

async function insertPost(data) {}

async function insertProposal(data) {}

async function insertVote(data) {}

async function updatePost(prev, data) {}

async function updateProposal(prev, data) {}

async function updateVote(prev, data) {}

module.exports = {
  getPost,
  listPostsByTopic,
  listPostsByUser,
  listVotesByProposal,
  insertPost,
  insertProposal,
  insertVote,
  updatePost,
  updateProposal,
  updateVote,
}
