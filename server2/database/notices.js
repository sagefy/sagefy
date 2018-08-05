const Joi = require('joi')
const db = require('./index')

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

/*
get_notice
  query = """
    SELECT *
    FROM notices
    WHERE id = %(id)s
    LIMIT 1;
  """

insert_notice
  query = """
    INSERT INTO notices
    (  user_id  ,   kind  ,   data  )
    VALUES
    (%(user_id)s, %(kind)s, %(data)s)
    RETURNING *;
  """

list_notices
  query = """
    SELECT *
    FROM notices
    WHERE user_id = %(user_id)s
    ORDER BY created DESC
    LIMIT %(limit)s
    OFFSET %(offset)s;
  """

mark_notice_as_read
  query = """
    UPDATE notices
    SET read = TRUE
    WHERE id = %(id)s
    RETURNING *;
  """

mark_notice_as_unread
  query = """
    UPDATE notices
    SET read = FALSE
    WHERE id = %(id)s
    RETURNING *;
  """
*/

async function getNotice(noticeId) {}

async function listNotices(userId, { limit = 10, offset = 0 }) {}

async function insertNotice(data) {}

async function updateNoticeAsRead(noticeId) {}

async function updateNoticeAsUnread(noticeId) {}

module.exports = {
  getNotice,
  listNotices,
  insertNotice,
  updateNoticeAsRead,
  updateNoticeAsUnread,
}
