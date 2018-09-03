const Joi = require('joi')

const db = require('./base')
const entitySchema = require('../helpers/entitySchema')

const unitSchema = entitySchema.keys({
  body: Joi.string(),
  require_ids: Joi.array().items(Joi.string().guid()),
})

async function doesUnitExist(entityId) {
  const query = `
    SELECT entity_id
    FROM units_entity_id
    WHERE entity_id = $entity_id
    LIMIT 1;
  `
}

async function getUnitVersion(versionId) {
  const query = `
    SELECT *
    FROM units
    WHERE version_id = $version_id
    ORDER BY created DESC;
  `
}

async function getLatestAcceptedUnit(entityId) {
  const query = `
    SELECT DISTINCT ON (entity_id) *
    FROM units
    WHERE status = 'accepted' AND entity_id = $entity_id
    ORDER BY entity_id, created DESC;
  `
}

async function listLatestAcceptedUnits(entityIds) {
  const query = `
    SELECT DISTINCT ON (entity_id) *
    FROM units
    WHERE status = 'accepted' AND entity_id in $entity_ids
    ORDER BY entity_id, created DESC;
  `
}

async function listOneUnitVersions(entityId) {
  const query = `
    SELECT *
    FROM units
    WHERE entity_id = $entity_id
    ORDER BY created DESC;
  `
}

async function listManyUnitVersions(versionIds) {
  const query = `
    SELECT *
    FROM units
    WHERE version_id in $version_ids
    ORDER BY created DESC;
  `
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
}

async function listUnitsBySubjectFlat(subjectId) {}

async function listMyRecentlyCreatedUnits(userId) {
  const query = `
    SELECT DISTINCT ON (entity_id) *
    FROM units
    WHERE user_id = $user_id
    ORDER BY entity_id, created DESC;
  `
}

async function listAllUnitEntityIds() {
  const query = `
    SELECT entity_id
    FROM units;
  `
}

async function insertUnit(data) {
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
}

async function insertUnitVersion(prev, data) {
  const query = `
    INSERT INTO units
    (  entity_id  ,   previous_id  ,   name  ,   user_id  ,
       body  ,   require_ids  )
    VALUES
    ($entity_id, $previous_id, $name, $user_id,
     $body, $require_ids)
    RETURNING *;
  `
}

async function updateUnit(versionId, status) {
  const query = `
    UPDATE units
    SET status = $status
    WHERE version_id = $version_id
    RETURNING *;
  `
}

module.exports = {
  doesUnitExist,
  getUnitVersion,
  getLatestAcceptedUnit,
  listLatestAcceptedUnits,
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
