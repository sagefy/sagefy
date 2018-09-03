const Joi = require('joi')
const db = require('./base')

const noticeSchema = Joi.object().keys({
  id: Joi.string().guid(),
  created: Joi.date(),
  modified: Joi.date(),
  user_id: Joi.string().guid(),
  kind: Joi.string().valid(
    'create_topic',
    'create_proposal',
    'block_proposal',
    'decline_proposal',
    'accept_proposal',
    'create_post',
    'come_back'
  ),
  data: Joi.object(),
  read: Joi.boolean(),
  tags: Joi.array().items(Joi.string().min(1)),
})

async function getNotice(noticeId) {
  const query = `
    SELECT *
    FROM notices
    WHERE id = $id
    LIMIT 1;
  `
}

async function listNotices(userId, { limit = 10, offset = 0 }) {
  const query = `
    SELECT *
    FROM notices
    WHERE user_id = $user_id
    ORDER BY created DESC
    LIMIT $limit
    OFFSET $offset;
  `
}

async function insertNotice(data) {
  const query = `
    INSERT INTO notices
    ( user_id,  kind,  data)
    VALUES
    ($user_id, $kind, $data)
    RETURNING *;
  `
}

async function updateNoticeAsRead(noticeId) {
  const query = `
    UPDATE notices
    SET read = TRUE
    WHERE id = $id
    RETURNING *;
  `
}

async function updateNoticeAsUnread(noticeId) {
  const query = `
    UPDATE notices
    SET read = FALSE
    WHERE id = $id
    RETURNING *;
  `
}

module.exports = {
  getNotice,
  listNotices,
  insertNotice,
  updateNoticeAsRead,
  updateNoticeAsUnread,
}
