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
