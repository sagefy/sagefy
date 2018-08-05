const Joi = require('joi')

const db = require('./index')
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

/*
insert_subject
  query = """
    INSERT INTO subjects_entity_id (entity_id)
    VALUES (%(entity_id)s);
    INSERT INTO subjects
    (  entity_id  ,   name  ,   user_id  ,
       body  ,   members  )
    VALUES
    (%(entity_id)s, %(name)s, %(user_id)s,
     %(body)s, %(members)s)
    RETURNING *;
  """

insert_subject_version
  query = """
    INSERT INTO subjects
    (  entity_id  ,   previous_id  ,   name  ,   user_id  ,
       body  ,   members  )
    VALUES
    (%(entity_id)s, %(previous_id)s, %(name)s, %(user_id)s,
     %(body)s, %(members)s)
    RETURNING *;
  """

update_subject
  query = """
    UPDATE subjects
    SET status = %(status)s
    WHERE version_id = %(version_id)s
    RETURNING *;
  """

does_subject_exist
  query = """
    SELECT entity_id
    FROM subjects_entity_id
    WHERE entity_id = %(entity_id)s
    LIMIT 1;
  """

get_latest_accepted_subject
  query = """
    SELECT DISTINCT ON (entity_id) *
    FROM subjects
    WHERE status = 'accepted' AND entity_id = %(entity_id)s
    ORDER BY entity_id, created DESC;
  """

list_latest_accepted_subjects
  query = """
    SELECT DISTINCT ON (entity_id) *
    FROM subjects
    WHERE status = 'accepted' AND entity_id in %(entity_ids)s
    ORDER BY entity_id, created DESC;
  """

list_many_subject_versions
  query = """
    SELECT *
    FROM subjects
    WHERE version_id in %(version_ids)s
    ORDER BY created DESC;
  """

get_subject_version
  query = """
    SELECT *
    FROM subjects
    WHERE version_id = %(version_id)s
    ORDER BY created DESC;
  """

list_one_subject_versions
  query = """
    SELECT *
    FROM subjects
    WHERE entity_id = %(entity_id)s
    ORDER BY created DESC;
  """

list_subjects_by_unit_flat
  # ENSURE THIS IS SQL SAFE
  unit_id = re.sub(r'[^a-zA-Z0-9\-\_]', '', unit_id)
  query = """
    WITH temp AS (
      SELECT DISTINCT ON (entity_id) *
      FROM subjects
      WHERE status = 'accepted'
      ORDER BY entity_id, created DESC
    )
    SELECT *
    FROM temp
    WHERE members @> '[{"id":"%(unit_id)s"}]'
    ORDER BY created DESC;
  """ % {'unit_id': unit_id}

list_subject_parents
  # ENSURE THIS IS SQL SAFE
  subject_id = re.sub(r'[^a-zA-Z0-9\-\_]', '', subject_id)
  query = """
    WITH temp AS (
      SELECT DISTINCT ON (entity_id) *
      FROM subjects
      WHERE status = 'accepted'
      ORDER BY entity_id, created DESC
    )
    SELECT *
    FROM temp
    WHERE members @> '[{"id":"%(subject_id)s"}]'
    ORDER BY created DESC;
  """ % {'subject_id': subject_id}

list_my_recently_created_subjects
  query = """
    SELECT DISTINCT ON (entity_id) *
    FROM subjects
    WHERE user_id = %(user_id)s
    ORDER BY entity_id, created DESC;
  """

list_all_subject_entity_ids
  query = """
    SELECT entity_id
    FROM subjects;
  """

get_recommended_subjects
  query = """
    SELECT DISTINCT ON (entity_id) *
    FROM subjects
    WHERE status = 'accepted' AND name = %(name)s
    ORDER BY entity_id, created DESC;
  """
*/

async function doesSubjectExist(entityId) {}

async function getSubjectVersion(versionId) {}

async function getLatestAcceptedSubject(entityId) {}

async function listLatestAcceptedSubjects(entityIds) {}

async function listManySubjectVersions(versionIds) {}

async function listOneSubjectVersions(entityId) {}

async function listSubjectsByUnitFlat(unitId) {}

async function listSubjectParents(subjectId) {}

async function listMyRecentlyCreatedSubjects(userId) {}

async function listAllSubjectEntityIds() {}

async function listRecommendedSubjects() {}

async function insertSubject(data) {}

async function insertSubjectVersion(prev, data) {}

async function updateSubject(versionId, status) {}

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
