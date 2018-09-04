const Joi = require('joi')

// TODO add additional checks on insert

const db = require('./base')
const es = require('../helpers/es')
const entitySchema = require('../helpers/entitySchema')

const subjectSchema = entitySchema.keys({
  body: Joi.string(),
  members: Joi.array().items(
    Joi.object.keys({
      id: Joi.string().length(22),
      kind: Joi.string().valid('unit', 'subject'),
    })
  ),
})

async function sendSubjectToEs(subject) {
  return es.index({
    index: 'entity',
    type: 'subject',
    body: subject,
    id: subject.entity_id,
  })
}

async function doesSubjectExist(entityId) {
  const query = `
    SELECT entity_id
    FROM subjects_entity_id
    WHERE entity_id = $entity_id
    LIMIT 1;
  `
  return db.get(query, { entity_id: entityId })
}

async function getSubjectVersion(versionId) {
  const query = `
    SELECT *
    FROM subjects
    WHERE version_id = $version_id
    ORDER BY created DESC;
  `
  return db.get(query, { version_id: versionId })
}

async function getLatestAcceptedSubject(entityId) {
  const query = `
    SELECT DISTINCT ON (entity_id) *
    FROM subjects
    WHERE status = 'accepted' AND entity_id = $entity_id
    ORDER BY entity_id, created DESC;
  `
  return db.get(query, { entity_id: entityId })
}

async function listLatestAcceptedSubjects(entityIds) {
  const query = `
    SELECT DISTINCT ON (entity_id) *
    FROM subjects
    WHERE status = 'accepted' AND entity_id = ANY ($entity_ids)
    ORDER BY entity_id, created DESC;
  `
  return db.list(query, { entity_ids: entityIds })
}

async function listManySubjectVersions(versionIds) {
  const query = `
    SELECT *
    FROM subjects
    WHERE version_id = ANY ($version_ids)
    ORDER BY created DESC;
  `
  return db.list(query, { version_ids: versionIds })
}

async function listOneSubjectVersions(entityId) {
  const query = `
    SELECT *
    FROM subjects
    WHERE entity_id = $entity_id
    ORDER BY created DESC;
  `
  return db.list(query, { entity_id: entityId })
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
  return db.list(query, { })
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
  return db.list(query, { })
  */
}

async function listMyRecentlyCreatedSubjects(userId) {
  const query = `
    SELECT DISTINCT ON (entity_id) *
    FROM subjects
    WHERE user_id = $user_id
    ORDER BY entity_id, created DESC;
  `
  return db.list(query, { user_id: userId })
}

async function listAllSubjectEntityIds() {
  const query = `
    SELECT entity_id
    FROM subjects;
  `
  return db.list(query)
}

async function listRecommendedSubjects() {
  const query = `
    SELECT DISTINCT ON (entity_id) *
    FROM subjects
    WHERE status = 'accepted' AND name = $name
    ORDER BY entity_id, created DESC;
  `
  return db.list(query, { name: 'An Introduction to Electronic Music' })
}

async function insertSubject(params) {
  Joi.assert(params, subjectSchema.requiredKeys(Object.keys(params)))
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
  const data = await db.save(query, params)
  await sendSubjectToEs(data)
  return data
}

async function insertSubjectVersion(params) {
  Joi.assert(params, subjectSchema.requiredKeys(Object.keys(params)))
  const query = `
    INSERT INTO subjects
    (  entity_id  ,   previous_id  ,   name  ,   user_id  ,
       body  ,   members  )
    VALUES
    ($entity_id, $previous_id, $name, $user_id,
     $body, $members)
    RETURNING *;
  `
  const data = await db.save(query, params)
  await sendSubjectToEs(data)
  return data
}

async function updateSubject(versionId, status) {
  const params = { version_id: versionId, status }
  Joi.assert(params, subjectSchema.requiredKeys(Object.keys(params)))
  const query = `
    UPDATE subjects
    SET status = $status
    WHERE version_id = $version_id
    RETURNING *;
  `
  const data = await db.save(query, params)
  await sendSubjectToEs(data)
  return data
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
