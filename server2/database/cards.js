const Joi = require('joi')

const db = require('./index')
const entitySchema = require('../helpers/entitySchema')

const cardSchema = entitySchema.keys({
  unit_id: Joi.string()
    .guid()
    .required(),
  require_ids: Joi.array()
    .items(Joi.string().guid())
    .required(),
  kind: Joi.string()
    .valid('video', 'page', 'unscored_embed', 'choice')
    .required(),
  data: Joi.object().required(),
})

const choiceCardSchema = cardSchema.keys({
  kind: Joi.string()
    .valid('choice')
    .required(),
  data: Joi.object()
    .keys({
      body: Joi.string().required(),
      options: Joi.array()
        .min(1)
        .items(
          Joi.object().keys({
            id: Joi.string()
              .guid()
              .required(),
            value: Joi.string().required(),
            correct: Joi.boolean().required(),
            feedback: Joi.string().required(),
          })
        )
        .required(),
      order: Joi.string()
        .valid('random', 'set')
        .required(),
      max_options_to_show: Joi.number()
        .integer()
        .required(),
    })
    .required(),
})

const pageCardSchema = cardSchema.keys({
  kind: Joi.string()
    .valid('page')
    .required(),
  data: Joi.object().keys({
    body: Joi.string().required(),
  }),
})

const videoCardSchema = cardSchema.keys({
  kind: Joi.string()
    .valid('video')
    .required(),
  data: Joi.object().keys({
    site: Joi.string()
      .valid('youtube', 'vimeo')
      .required(),
    video_id: Joi.string().required(),
  }),
})

const unscoredEmbedCardSchema = cardSchema.keys({
  kind: Joi.string()
    .valid('unscored_embed')
    .required(),
  data: Joi.object().keys({
    url: Joi.string()
      .uri()
      .required(),
  }),
})

const cardParametersSchema = Joi.object().keys({
  id: Joi.string()
    .guid()
    .required(),
  created: Joi.date().required(),
  modified: Joi.date().required(),
  entity_id: Joi.string()
    .guid()
    .required(),
  guess_distribution: Joi.object()
    .pattern(
      /^\d*\.?\d*$/,
      Joi.number()
        .min(0)
        .max(1)
        .required()
    )
    .required(),
  slip_distribution: Joi.object()
    .pattern(
      /^\d*\.?\d*$/,
      Joi.number()
        .min(0)
        .max(1)
        .required()
    )
    .required(),
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
