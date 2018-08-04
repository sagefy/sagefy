const db = require('./index')

/*

CREATE TABLE subjects_entity_id (
  entity_id uuid PRIMARY KEY DEFAULT uuid_generate_v4()
);

CREATE TABLE subjects (
  version_id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  modified timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  entity_id uuid NOT NULL REFERENCES subjects_entity_id (entity_id),
  previous_id uuid NULL REFERENCES subjects (version_id),
  language varchar(5)    NOT NULL DEFAULT 'en'
    CONSTRAINT lang_check CHECK (language ~* '^\w{2}(-\w{2})?$'),
  name text NOT NULL,
  status entity_status NOT NULL DEFAULT 'pending',
  available boolean NOT NULL DEFAULT TRUE,
  tags text[] NULL DEFAULT array[]::text[],
  user_id uuid NOT NULL REFERENCES users (id),
  --- and the rest....
  body text NOT NULL,
  members jsonb NOT NULL --- jsonb?: ISSUE cant ref, cant enum composite
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
  'tablename': 'subjects',
  'fields': {
    'body': {
      'validate': (is_required, is_string,),
    },
    'members': {
      'validate': (is_required, is_list,),
      'embed_many': {
        'id': {
          'validate': (is_required, is_string,),
        },
        'kind': {
          'validate': (is_required, is_string, (
            is_one_of, 'unit', 'subject'
          )),
        }
      }
    }
  },
})

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
