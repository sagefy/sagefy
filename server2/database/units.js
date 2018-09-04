const Joi = require('joi')

// TODO add additional checks on insert

const db = require('./base')
const es = require('../helpers/es')
const entitySchema = require('../helpers/entitySchema')

const unitSchema = entitySchema.keys({
  body: Joi.string(),
  require_ids: Joi.array().items(Joi.string().length(22)),
})

async function sendUnitToEs(unit) {
  return es.index({
    index: 'entity',
    type: 'unit',
    body: unit,
    id: unit.entity_id,
  })
}

async function doesUnitExist(entityId) {
  const query = `
    SELECT entity_id
    FROM units_entity_id
    WHERE entity_id = $entity_id
    LIMIT 1;
  `
  return db.get(query, { entity_id: entityId })
}

async function getUnitVersion(versionId) {
  const query = `
    SELECT *
    FROM units
    WHERE version_id = $version_id
    ORDER BY created DESC;
  `
  return db.get(query, { version_id: versionId })
}

async function getLatestAcceptedUnit(entityId) {
  const query = `
    SELECT DISTINCT ON (entity_id) *
    FROM units
    WHERE status = 'accepted' AND entity_id = $entity_id
    ORDER BY entity_id, created DESC;
  `
  return db.get(query, { entity_id: entityId })
}

async function listLatestAcceptedUnits(entityIds) {
  const query = `
    SELECT DISTINCT ON (entity_id) *
    FROM units
    WHERE status = 'accepted' AND entity_id = ANY ($entity_ids)
    ORDER BY entity_id, created DESC;
  `
  return db.list(query, { entity_ids: entityIds })
}

async function listOneUnitVersions(entityId) {
  const query = `
    SELECT *
    FROM units
    WHERE entity_id = $entity_id
    ORDER BY created DESC;
  `
  return db.list(query, { entity_id: entityId })
}

async function listManyUnitVersions(versionIds) {
  const query = `
    SELECT *
    FROM units
    WHERE version_id = ANY ($version_ids)
    ORDER BY created DESC;
  `
  return db.list(query, { version_ids: versionIds })
}

async function listRequiredUnits(entityId) {}

async function listRequiredByUnits(entityId) {
  const query = `
    WITH temp as (
      SELECT DISTINCT ON (entity_id) *
      FROM units
      WHERE status = 'accepted'
      ORDER BY entity_id, created DESC
    )
    SELECT *
    FROM temp
    WHERE $entity_id = ANY(require_ids)
    ORDER BY created DESC;
  `
  return db.list(query, { entity_id: entityId })
}

async function listUnitsBySubjectFlat(subjectId) {}

async function listMyRecentlyCreatedUnits(userId) {
  const query = `
    SELECT DISTINCT ON (entity_id) *
    FROM units
    WHERE user_id = $user_id
    ORDER BY entity_id, created DESC;
  `
  return db.list(query, { user_id: userId })
}

async function listAllUnitEntityIds() {
  const query = `
    SELECT entity_id
    FROM units;
  `
  return db.list(query)
}

async function insertUnit(params) {
  Joi.assert(params, unitSchema.requiredKeys(Object.keys(params)))
  const query = `
    INSERT INTO units_entity_id (entity_id)
    VALUES ($entity_id);
    INSERT INTO units
    (  entity_id  ,   name  ,   user_id  ,
       body  ,   require_ids  )
    VALUES
    ($entity_id  , $name, $user_id,
     $body, $require_ids)
    RETURNING *;
  `
  const data = await db.save(query, params)
  await sendUnitToEs(data)
  return data
}

async function insertUnitVersion(params) {
  Joi.assert(params, unitSchema.requiredKeys(Object.keys(params)))
  const query = `
    INSERT INTO units
    (  entity_id  ,   previous_id  ,   name  ,   user_id  ,
       body  ,   require_ids  )
    VALUES
    ($entity_id, $previous_id, $name, $user_id,
     $body, $require_ids)
    RETURNING *;
  `
  const data = await db.save(query, params)
  await sendUnitToEs(data)
  return data
}

async function updateUnit(versionId, status) {
  const params = { version_id: versionId, status }
  Joi.assert(params, unitSchema.requiredKeys(Object.keys(params)))
  const query = `
    UPDATE units
    SET status = $status
    WHERE version_id = $version_id
    RETURNING *;
  `
  const data = await db.save(query, params)
  await sendUnitToEs(data)
  return data
}

module.exports = {
  doesUnitExist,
  getUnitVersion,
  getLatestAcceptedUnit,
  listLatestAcceptedUnits,
  listOneUnitVersions,
  listManyUnitVersions,
  listRequiredUnits,
  listRequiredByUnits,
  listUnitsBySubjectFlat,
  listMyRecentlyCreatedUnits,
  listAllUnitEntityIds,
  insertUnit,
  insertUnitVersion,
  updateUnit,
}
