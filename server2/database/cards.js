const Joi = require('joi')

const db = require('./index')
const entitySchema = require('../helpers/entitySchema')

const cardSchema = entitySchema.keys({
  unit_id: Joi.string().guid(),
  require_ids: Joi.array().items(Joi.string().guid()),
  kind: Joi.string().valid('video', 'page', 'unscored_embed', 'choice'),
  data: Joi.object(),
})

const choiceCardSchema = cardSchema.keys({
  kind: Joi.string().valid('choice'),
  data: Joi.object().keys({
    body: Joi.string(),
    options: Joi.array()
      .min(1)
      .items(
        Joi.object().keys({
          id: Joi.string().guid(),
          value: Joi.string(),
          correct: Joi.boolean(),
          feedback: Joi.string(),
        })
      ),
    order: Joi.string().valid('random', 'set'),
    max_options_to_show: Joi.number().integer(),
  }),
})

const pageCardSchema = cardSchema.keys({
  kind: Joi.string().valid('page'),
  data: Joi.object().keys({
    body: Joi.string(),
  }),
})

const videoCardSchema = cardSchema.keys({
  kind: Joi.string().valid('video'),
  data: Joi.object().keys({
    site: Joi.string().valid('youtube', 'vimeo'),
    video_id: Joi.string(),
  }),
})

const unscoredEmbedCardSchema = cardSchema.keys({
  kind: Joi.string().valid('unscored_embed'),
  data: Joi.object().keys({
    url: Joi.string().uri(),
  }),
})

const cardParametersSchema = Joi.object().keys({
  id: Joi.string().guid(),
  created: Joi.date(),
  modified: Joi.date(),
  entity_id: Joi.string().guid(),
  guess_distribution: Joi.object().pattern(
    /^\d*\.?\d*$/,
    Joi.number()
      .min(0)
      .max(1)
  ),
  slip_distribution: Joi.object().pattern(
    /^\d*\.?\d*$/,
    Joi.number()
      .min(0)
      .max(1)
  ),
})

async function getCardVersion(versionId) {}

async function getLatestAcceptedCard(entityId) {}

async function getCardParameters(entityId) {}

async function listLatestAcceptedCards(entityId) {}

async function listManyCardVersions(versionIds) {}

async function listOneCardVersions(entityId) {}

async function listRequiredCards(entityId) {}

async function listRequiredByCards(entityId) {}

async function listRandomCardsInUnit(unitId, { limit = 10 }) {}

async function listAllCardEntityIds() {}

async function insertCard(data) {}

async function insertCardVersion(prev, data) {}

async function insertCardParameters(data) {}

async function updateCard(versionId, status) {}

async function updateCardParameters(prev, data) {}

module.exports = {
  getCardVersion,
  getLatestAcceptedCard,
  getCardParameters,
  listLatestAcceptedCards,
  listManyCardVersions,
  listOneCardVersions,
  listRequiredCards,
  listRequiredByCards,
  listRandomCardsInUnit,
  listAllCardEntityIds,
  insertCard,
  insertCardVersion,
  insertCardParameters,
  updateCard,
  updateCardParameters,
}
