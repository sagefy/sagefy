const Joi = require('joi')

const db = require('./base')
const entitySchema = require('../helpers/entitySchema')

const subjectSchema = entitySchema.keys({
  body: Joi.string(),
  members: Joi.array().items(
    Joi.object.keys({
      id: Joi.string().guid(),
      kind: Joi.string().valid('unit', 'subject'),
    })
  ),
})

async function doesSubjectExist(entityId) {
  const query = `
    SELECT entity_id
    FROM subjects_entity_id
    WHERE entity_id = $entity_id
    LIMIT 1;
  `
}

async function getSubjectVersion(versionId) {
  const query = `
    SELECT *
    FROM subjects
    WHERE version_id = $version_id
    ORDER BY created DESC;
  `
}

async function getLatestAcceptedSubject(entityId) {
  const query = `
    SELECT DISTINCT ON (entity_id) *
    FROM subjects
    WHERE status = 'accepted' AND entity_id = $entity_id
    ORDER BY entity_id, created DESC;
  `
}

async function listLatestAcceptedSubjects(entityIds) {
  const query = `
    SELECT DISTINCT ON (entity_id) *
    FROM subjects
    WHERE status = 'accepted' AND entity_id in $entity_ids
    ORDER BY entity_id, created DESC;
  `
}

async function listManySubjectVersions(versionIds) {
  const query = `
    SELECT *
    FROM subjects
    WHERE version_id in $version_ids
    ORDER BY created DESC;
  `
}

async function listOneSubjectVersions(entityId) {
  const query = `
    SELECT *
    FROM subjects
    WHERE entity_id = $entity_id
    ORDER BY created DESC;
  `
}

async function listSubjectsByUnitFlat(unitId) {
  /*
  # ENSURE THIS IS SQL SAFE
  unit_id = re.sub(r'[^a-zA-Z0-9\-\_]', '', unit_id)
  const query = `
    WITH temp AS (
      SELECT DISTINCT ON (entity_id) *
      FROM subjects
      WHERE status = 'accepted'
      ORDER BY entity_id, created DESC
    )
    SELECT *
    FROM temp
    WHERE members @> '[{"id":"$unit_id"}]'
    ORDER BY created DESC;
  ` % {'unit_id': unit_id}
  */
}

async function listSubjectParents(subjectId) {
  /*
  # ENSURE THIS IS SQL SAFE
  subject_id = re.sub(r'[^a-zA-Z0-9\-\_]', '', subject_id)
  const query = `
    WITH temp AS (
      SELECT DISTINCT ON (entity_id) *
      FROM subjects
      WHERE status = 'accepted'
      ORDER BY entity_id, created DESC
    )
    SELECT *
    FROM temp
    WHERE members @> '[{"id":"$subject_id"}]'
    ORDER BY created DESC;
  ` % {'subject_id': subject_id}
  */
}

async function listMyRecentlyCreatedSubjects(userId) {
  const query = `
    SELECT DISTINCT ON (entity_id) *
    FROM subjects
    WHERE user_id = $user_id
    ORDER BY entity_id, created DESC;
  `
}

async function listAllSubjectEntityIds() {
  const query = `
    SELECT entity_id
    FROM subjects;
  `
}

async function listRecommendedSubjects() {
  const query = `
    SELECT DISTINCT ON (entity_id) *
    FROM subjects
    WHERE status = 'accepted' AND name = $name
    ORDER BY entity_id, created DESC;
  `
}

async function insertSubject(data) {
  const query = `
    INSERT INTO subjects_entity_id (entity_id)
    VALUES ($entity_id);
    INSERT INTO subjects
    (  entity_id  ,   name  ,   user_id  ,
       body  ,   members  )
    VALUES
    ($entity_id, $name, $user_id,
     $body, $members)
    RETURNING *;
  `
}

async function insertSubjectVersion(prev, data) {
  const query = `
    INSERT INTO subjects
    (  entity_id  ,   previous_id  ,   name  ,   user_id  ,
       body  ,   members  )
    VALUES
    ($entity_id, $previous_id, $name, $user_id,
     $body, $members)
    RETURNING *;
  `
}

async function updateSubject(versionId, status) {
  const query = `
    UPDATE subjects
    SET status = $status
    WHERE version_id = $version_id
    RETURNING *;
  `
}

module.exports = {
  doesSubjectExist,
  getSubjectVersion,
  getLatestAcceptedSubject,
  listLatestAcceptedSubjects,
  listManySubjectVersions,
  listOneSubjectVersions,
  listSubjectsByUnitFlat,
  listSubjectParents,
  listMyRecentlyCreatedSubjects,
  listAllSubjectEntityIds,
  listRecommendedSubjects,
  insertSubject,
  insertSubjectVersion,
  updateSubject,
}
