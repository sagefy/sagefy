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
