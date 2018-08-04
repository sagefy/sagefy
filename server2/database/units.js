const db = require('./index')

/*

CREATE TABLE units_entity_id (
  entity_id uuid PRIMARY KEY DEFAULT uuid_generate_v4()
);

CREATE TABLE units (
  version_id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  modified timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  entity_id uuid NOT NULL REFERENCES units_entity_id (entity_id),
  previous_id uuid NULL REFERENCES units (version_id),
  language varchar(5) NOT NULL DEFAULT 'en'
    CONSTRAINT lang_check CHECK (language ~* '^\w{2}(-\w{2})?$'),
  name text NOT NULL,
  status entity_status NOT NULL DEFAULT 'pending',
  available boolean NOT NULL DEFAULT TRUE,
  tags text[] NULL DEFAULT array[]::text[],
  user_id uuid NOT NULL REFERENCES users (id),
  --- and the rest.... ---
  body text NOT NULL,
  require_ids uuid[] NOT NULL DEFAULT array[]::uuid[] --- ISSUE no ELEMENT
);


schema = extend({}, default, {
  'fields': {
    'version_id': {
      'validate': (is_uuid,),
    },
    'entity_id': {
      'validate': (is_required, is_uuid,),
    },
    'previous_id': {
      'validate': (is_uuid,),
    },
    'language': {
      'validate': (is_required, is_string, is_language,),
      'default': 'en',
    },
    'name': {
      'validate': (is_required, is_string,),
    },
    'status': {
      'validate': (
        is_required,
        is_string,
        (
          is_one_of,
          'pending',
          'blocked',
          'declined',
          'accepted'
        ),
      ),
      'default': 'pending',
    },
    'available': {
      'validate': (is_required, is_boolean,),
      'default': True,
    },
    'tags': {
      'validate': (is_list, is_list_of_strings,),
      'default': [],
    },
    'user_id': {
      'validate': (is_required, is_uuid,),
    },
  },
})

schema = extend({}, entity_schema, {
  'tablename': 'units',
  'fields': {
    'body': {
      'validate': (is_required, is_string,),
    },
    'require_ids': {
      'validate': (is_required, is_list, is_list_of_uuids),
      'default': [],
    },
  },
})


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
