const db = require('./index')

/*


CREATE TABLE cards_entity_id (
  entity_id uuid PRIMARY KEY DEFAULT uuid_generate_v4()
);

CREATE TABLE cards (
  version_id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  modified timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  entity_id uuid NOT NULL REFERENCES cards_entity_id (entity_id),
  previous_id uuid NULL REFERENCES cards (version_id),
  language varchar(5) NOT NULL DEFAULT 'en'
    CONSTRAINT lang_check CHECK (language ~* '^\w{2}(-\w{2})?$'),
  name text NOT NULL,
  status entity_status NOT NULL DEFAULT 'pending',
  available boolean NOT NULL DEFAULT TRUE,
  tags text[] NULL DEFAULT array[]::text[],
  user_id uuid NOT NULL REFERENCES users (id),
  --- and the rest....
  unit_id uuid NOT NULL REFERENCES units_entity_id (entity_id),
  require_ids uuid[] NOT NULL DEFAULT array[]::uuid[], --- ISSUE no ELEMENT
  kind card_kind NOT NULL,
  data jsonb NOT NULL --- jsonb?: varies per kind
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


scored_kinds = ('choice',)

peer_scored_kinds = tuple()

schema = extend({}, entity_schema, {
  'tablename': 'cards',
  'fields': {
    'unit_id': {
      'validate': (is_required, is_uuid,)
    },
    'require_ids': {
      'validate': (is_required, is_list, is_list_of_uuids),
      'default': [],
    },
    'kind': {
      'validate': (
        is_required,
        is_string,
        (
          is_one_of,
          'video',
          'page',
          'unscored_embed',
          'choice'
        )
      ),
    },
    'data': {
      'validate': (is_required, is_dict,),
      'default': {},
    },
  },
})


schema = extend({}, card_schema, {
  'fields': {
    'data': {
      'embed': {
        'body': {  # Question field
          'validate': (is_required, is_string,),
        },
        'options': {  # Available answers
          'validate': (is_required, is_list, (has_min_length, 1), has_correct_options),
          'embed_many': {
            'id': {
              'validate': (is_required, is_string,),
              'default': create_uuid_b64,
            },
            'value': {
              'validate': (is_required, is_string,),
            },
            'correct': {
              'validate': (is_required, is_boolean,),
              'access': ('view',),
            },
            'feedback': {
              'validate': (is_required, is_string,),
              'access': ('view',),
            },
          }
        },
        'order': {
          'validate': (is_string, (is_one_of, 'random', 'set')),
          'default': 'random',
          'access': ('view',),
        },
        'max_options_to_show': {
          'validate': (is_integer,),
          'default': 4,
          'access': ('view',),
        },
      },
    },
  },
})


schema = extend({}, card_schema, {
  'fields': {
    'data': {
      'body': {
        'validate': (is_required, is_string,)
      },
    },
  }
})


schema = extend({}, card_schema, {
  'fields': {
    'data': {
      'url': {
        'validate': (is_required, is_string, is_url,)
      },
    },
  }
})


schema = extend({}, card_schema, {
  'fields': {
    'data': {
      'embed': {
        'site': {
          'validate': (is_required, is_string, (is_one_of, 'youtube', 'vimeo'),),
        },
        'video_id': {
          'validate': (is_required, is_string,),
        },
      },
    },
  },
})



CREATE TABLE cards_parameters (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  modified timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  entity_id uuid NOT NULL UNIQUE REFERENCES cards_entity_id (entity_id),
  guess_distribution jsonb NOT NULL,
    --- jsonb?: map
  slip_distribution jsonb NOT NULL );


schema = extend({}, default, {
  'tablename': 'cards_parameters',
  'fields': {
    'entity_id': {
      'validate': (is_required, is_uuid,)
    },
    'guess_distribution': {
      'validate': (is_required, is_dict,)
    },
    'slip_distribution': {
      'validate': (is_required, is_dict,)
    },
  },
})

*/

async function getCardVersion(versionId) {}

async function getLatestAcceptedCard(entityId) {}

async function getCardParameters(entityId) {}

async function listLatestAcceptedCards(entityId) {}

async function listManyCardVersions(versionIds) {}

async function listOneCardVersions(entityId) {}

async function listRequiredCards(entityId) {}

async function listRequiredByCards(entityId) {}

async function listRandomCardsInUnit(unitId, { limit = 10 }) {}

async function listAllCardEntityIds() {}

async function insertCard(data) {}

async function insertCardVersion(prev, data) {}

async function insertCardParameters(data) {}

async function updateCard(versionId, status) {}

async function updateCardParameters(prev, data) {}

module.exports = {
  getCardVersion,
  getLatestAcceptedCard,
  getCardParameters,
  listLatestAcceptedCards,
  listManyCardVersions,
  listOneCardVersions,
  listRequiredCards,
  listRequiredByCards,
  listRandomCardsInUnit,
  listAllCardEntityIds,
  insertCard,
  insertCardVersion,
  insertCardParameters,
  updateCard,
  updateCardParameters,
}
