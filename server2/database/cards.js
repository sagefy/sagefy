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

/*
get_card_parameters
  query = """
    SELECT *
    FROM cards_parameters
    WHERE entity_id = %(entity_id)s
    LIMIT 1;
  """

insert_card_parameters
  query = """
    INSERT INTO cards_parameters
    (  entity_id  ,   guess_distribution  ,   slip_distribution  )
    VALUES
    (%(entity_id)s, %(guess_distribution)s, %(slip_distribution)s)
    RETURNING *;
  """

update_card_parameters
  query = """
    UPDATE cards_parameters
    SET guess_distribution = %(guess_distribution)s,
      slip_distribution = %(slip_distribution)s
    WHERE entity_id = %(entity_id)s
    RETURNING *;
  """

insert_card
  query = """
    INSERT INTO cards_entity_id (entity_id)
    VALUES (%(entity_id)s);
    INSERT INTO cards
    (  entity_id  ,   name  ,   user_id  ,   unit_id  ,
       require_ids  ,   kind  ,   data  )
    VALUES
    (%(entity_id)s, %(name)s, %(user_id)s, %(unit_id)s,
     %(require_ids)s, %(kind)s, %(data)s)
    RETURNING *;
  """

insert_card_version
  query = """
    INSERT INTO cards
    (  entity_id  ,   previous_id  ,   name  ,   user_id  ,   unit_id  ,
       require_ids  ,   kind  ,   data  )
    VALUES
    (%(entity_id)s, %(previous_id)s, %(name)s, %(user_id)s, %(unit_id)s,
     %(require_ids)s, %(kind)s, %(data)s)
    RETURNING *;
  """

update_card
  query = """
    UPDATE cards
    SET status = %(status)s
    WHERE version_id = %(version_id)s
    RETURNING *;
  """

get_latest_accepted_card
  query = """
    SELECT DISTINCT ON (entity_id) *
    FROM cards
    WHERE status = 'accepted' AND entity_id = %(entity_id)s
    ORDER BY entity_id, created DESC;
  """

list_latest_accepted_cards
  query = """
    SELECT DISTINCT ON (entity_id) *
    FROM cards
    WHERE status = 'accepted' AND entity_id in %(entity_ids)s
    ORDER BY entity_id, created DESC;
  """

list_many_card_versions
  query = """
    SELECT *
    FROM cards
    WHERE version_id in %(version_ids)s
    ORDER BY created DESC;
  """

get_card_version
  query = """
    SELECT *
    FROM cards
    WHERE version_id = %(version_id)s
    ORDER BY created DESC;
  """

list_one_card_versions
  query = """
    SELECT *
    FROM cards
    WHERE entity_id = %(entity_id)s
    ORDER BY created DESC;
  """

list_required_by_cards
  query = """
    WITH temp as (
      SELECT DISTINCT ON (entity_id) *
      FROM cards
      WHERE status = 'accepted'
      ORDER BY entity_id, created DESC
    )
    SELECT *
    FROM temp
    WHERE %(entity_id)s = ANY(require_ids)
    ORDER BY created DESC;
  """
*/

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
