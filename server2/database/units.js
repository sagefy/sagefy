const Joi = require('joi')

const db = require('./index')
const entitySchema = require('../helpers/entitySchema')

const unitSchema = entitySchema.keys({
  body: Joi.string().required(),
  require_ids: Joi.array()
    .items(Joi.string().guid())
    .required(),
})

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
