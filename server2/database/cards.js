const Joi = require('joi')

const db = require('./base')
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

async function getCardVersion(versionId) {
  const query = `
    SELECT *
    FROM cards
    WHERE version_id = $version_id
    ORDER BY created DESC;
  `
}

async function getLatestAcceptedCard(entityId) {
  const query = `
    SELECT DISTINCT ON (entity_id) *
    FROM cards
    WHERE status = 'accepted' AND entity_id = $entity_id
    ORDER BY entity_id, created DESC;
  `
}

async function getCardParameters(entityId) {
  const query = `
    SELECT *
    FROM cards_parameters
    WHERE entity_id = $entity_id
    LIMIT 1;
  `
}

async function listLatestAcceptedCards(entityId) {
  const query = `
    SELECT DISTINCT ON (entity_id) *
    FROM cards
    WHERE status = 'accepted' AND entity_id in $entity_ids
    ORDER BY entity_id, created DESC;
  `
}

async function listManyCardVersions(versionIds) {
  const query = `
    SELECT *
    FROM cards
    WHERE version_id in $version_ids
    ORDER BY created DESC;
  `
}

async function listOneCardVersions(entityId) {
  const query = `
    SELECT *
    FROM cards
    WHERE entity_id = $entity_id
    ORDER BY created DESC;
  `
}

async function listRequiredCards(entityId) {}

async function listRequiredByCards(entityId) {
  const query = `
    WITH temp as (
      SELECT DISTINCT ON (entity_id) *
      FROM cards
      WHERE status = 'accepted'
      ORDER BY entity_id, created DESC
    )
    SELECT *
    FROM temp
    WHERE $entity_id = ANY(require_ids)
    ORDER BY created DESC;
  `
}

async function listRandomCardsInUnit(unitId, { limit = 10 }) {
  const query = `
    WITH temp as (
      SELECT DISTINCT ON (entity_id) *
      FROM cards
      WHERE status = 'accepted'
      ORDER BY entity_id, created DESC
    )
    SELECT *
    FROM temp
    WHERE unit_id = $unit_id
    ORDER BY random()
    LIMIT $limit;
  `
}

async function listAllCardEntityIds() {
  const query = `
    SELECT entity_id
    FROM cards;
  `
}

async function insertCard(data) {
  const query = `
    INSERT INTO cards_entity_id (entity_id)
    VALUES ($entity_id);
    INSERT INTO cards
    (  entity_id  ,   name  ,   user_id  ,   unit_id  ,
       require_ids  ,   kind  ,   data  )
    VALUES
    ($entity_id, $name, $user_id, $unit_id,
     $require_ids, $kind, $data)
    RETURNING *;
  `
}

async function insertCardVersion(prev, data) {
  const query = `
    INSERT INTO cards
    (  entity_id  ,   previous_id  ,   name  ,   user_id  ,   unit_id  ,
       require_ids  ,   kind  ,   data  )
    VALUES
    ($entity_id, $previous_id, $name, $user_id, $unit_id,
     $require_ids, $kind, $data)
    RETURNING *;
  `
}

async function insertCardParameters(data) {
  const query = `
    INSERT INTO cards_parameters
    (  entity_id  ,   guess_distribution  ,   slip_distribution  )
    VALUES
    ($entity_id, $guess_distribution, $slip_distribution)
    RETURNING *;
  `
}

async function updateCard(versionId, status) {
  const query = `
    UPDATE cards
    SET status = $status
    WHERE version_id = $version_id
    RETURNING *;
  `
}

async function updateCardParameters(prev, data) {
  const query = `
    UPDATE cards_parameters
    SET guess_distribution = $guess_distribution,
      slip_distribution = $slip_distribution
    WHERE entity_id = $entity_id
    RETURNING *;
  `
}

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
