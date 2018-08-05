const Joi = require('joi')

const db = require('./index')
const entitySchema = require('../helpers/entitySchema')

const unitSchema = entitySchema.keys({
  body: Joi.string(),
  require_ids: Joi.array().items(Joi.string().guid()),
})

/*
insert_unit
  query = """
    INSERT INTO units_entity_id (entity_id)
    VALUES (%(entity_id)s);
    INSERT INTO units
    (  entity_id  ,   name  ,   user_id  ,
       body  ,   require_ids  )
    VALUES
    (%(entity_id)s  , %(name)s, %(user_id)s,
     %(body)s, %(require_ids)s)
    RETURNING *;
  """

insert_unit_version
  query = """
    INSERT INTO units
    (  entity_id  ,   previous_id  ,   name  ,   user_id  ,
       body  ,   require_ids  )
    VALUES
    (%(entity_id)s, %(previous_id)s, %(name)s, %(user_id)s,
     %(body)s, %(require_ids)s)
    RETURNING *;
  """

update_unit
  query = """
    UPDATE units
    SET status = %(status)s
    WHERE version_id = %(version_id)s
    RETURNING *;
  """

does_unit_exist
  query = """
    SELECT entity_id
    FROM units_entity_id
    WHERE entity_id = %(entity_id)s
    LIMIT 1;
  """

get_latest_accepted_unit
  query = """
    SELECT DISTINCT ON (entity_id) *
    FROM units
    WHERE status = 'accepted' AND entity_id = %(entity_id)s
    ORDER BY entity_id, created DESC;
  """

list_latest_accepted_units
  query = """
    SELECT DISTINCT ON (entity_id) *
    FROM units
    WHERE status = 'accepted' AND entity_id in %(entity_ids)s
    ORDER BY entity_id, created DESC;
  """

list_many_unit_versions
  query = """
    SELECT *
    FROM units
    WHERE version_id in %(version_ids)s
    ORDER BY created DESC;
  """

get_unit_version
  query = """
    SELECT *
    FROM units
    WHERE version_id = %(version_id)s
    ORDER BY created DESC;
  """

list_one_unit_versions
  query = """
    SELECT *
    FROM units
    WHERE entity_id = %(entity_id)s
    ORDER BY created DESC;
  """

list_required_by_units
  query = """
    WITH temp as (
      SELECT DISTINCT ON (entity_id) *
      FROM units
      WHERE status = 'accepted'
      ORDER BY entity_id, created DESC
    )
    SELECT *
    FROM temp
    WHERE %(entity_id)s = ANY(require_ids)
    ORDER BY created DESC;
  """

list_my_recently_created_units
  query = """
    SELECT DISTINCT ON (entity_id) *
    FROM units
    WHERE user_id = %(user_id)s
    ORDER BY entity_id, created DESC;
  """

list_all_unit_entity_ids
  query = """
    SELECT entity_id
    FROM units;
  """
*/

async function doesUnitExist(entityId) {}

async function getUnitVersion(versionId) {}

async function getLatestAcceptedUnit(entityId) {}

async function listLatestAcceptedUnits(entityIds) {}

async function listManyUnitVersions(versionIds) {}

async function listRequiredUnits(entityId) {}

async function listRequiredByUnits(entityId) {}

async function listUnitsBySubjectFlat(subjectId) {}

async function listMyRecentlyCreatedUnits(userId) {}

async function listAllUnitEntityIds() {}

async function insertUnit(data) {}

async function insertUnitVersion(prev, data) {}

async function updateUnit(versionId, status) {}

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
