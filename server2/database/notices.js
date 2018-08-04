const Joi = require('joi')
const db = require('./index')

const noticeSchema = Joi.object().keys({
  id: Joi.string()
    .guid()
    .required(),
  created: Joi.date().required(),
  modified: Joi.date().required(),
  user_id: Joi.string()
    .guid()
    .required(),
  kind: Joi.string()
    .valid(
      'create_topic',
      'create_proposal',
      'block_proposal',
      'decline_proposal',
      'accept_proposal',
      'create_post',
      'come_back'
    )
    .required(),
  data: Joi.object().required(),
  read: Joi.boolean().required(),
  tags: Joi.array()
    .items(Joi.string().min(1))
    .required(),
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
