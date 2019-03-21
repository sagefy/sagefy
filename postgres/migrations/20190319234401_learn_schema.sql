-- migrate:up

create or replace function sg_private.insert_user_or_session()
returns trigger as $$
begin
  if (current_setting('jwt.claims.user_id') is not null
      and current_setting('jwt.claims.user_id') <> '') then
    new.user_id = current_setting('jwt.claims.user_id')::uuid;
  elsif (current_setting('jwt.claims.session_id') is not null
      and current_setting('jwt.claims.session_id') <> '') then
    new.session_id = current_setting('jwt.claims.session_id')::uuid;
  end if;
  return new;
end;
$$ language plpgsql strict security definer;
comment on function sg_private.insert_user_or_session()
  is 'When inserting a row, automatically set the `user_id` or `session_id` field.';

create type sg_public.entity_kind as enum(
  'card',
  'subject'
);
comment on type sg_public.entity_kind
  is 'The types of learning entities.';

create type sg_public.entity_status as enum(
  'pending',
  'blocked',
  'declined',
  'accepted'
);
comment on type sg_public.entity_status
  is 'The four statuses of entity versions.';

create type sg_public.card_kind as enum(
  'video',
  'page',
  'unscored_embed',
  'choice'
);
comment on type sg_public.card_kind
  is 'The kinds of cards available to learn. Expanding.';

create table sg_public.entity (
  entity_id uuid primary key default uuid_generate_v4(),
  entity_kind sg_public.entity_kind not null,
  unique (entity_id, entity_kind)
);

comment on table sg_public.entity
  is 'A list of all entity IDs and their kinds.';
comment on column sg_public.entity.entity_id
  is 'The overall ID of the entity.';
comment on column sg_public.entity.entity_kind
  is 'The kind of entity the ID represents.';

create table sg_public.entity_version (
  version_id uuid primary key default uuid_generate_v4(),
  entity_kind sg_public.entity_kind not null,
  unique (version_id, entity_kind)
);

comment on table sg_public.entity_version
  is 'A list of all entity version IDs and their kinds.';
comment on column sg_public.entity_version.version_id
  is 'The ID of the version.';
comment on column sg_public.entity_version.entity_kind
  is 'The kind of entity the ID represents.';

create table sg_public.subject_entity (
  entity_id uuid primary key references sg_public.entity (entity_id)
);

comment on table sg_public.subject_entity
  is 'A list of all subject entity IDs.';
comment on column sg_public.subject_entity.entity_id
  is 'The ID of the entity.';

create table sg_public.subject_version (
  -- all entity columns
  version_id uuid primary key references sg_public.entity_version (version_id),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  entity_id uuid not null references sg_public.subject_entity (entity_id),
  previous_version_id uuid null references sg_public.subject_version (version_id),
  language varchar(5) not null default 'en'
    constraint lang_check check (language ~* '^\w{2}(-\w{2})?$'),
  name text not null,
  status sg_public.entity_status not null default 'pending',
  available boolean not null default true,
  tags text[] null default array[]::text[],
  user_id uuid null references sg_public.user (id),
  session_id uuid null,
  -- and the rest....
  body text not null,
  -- also see join table: sg_public.subject_version_parent_child
  -- also see join table: sg_public.subject_version_before_after
  constraint user_or_session check (user_id is not null or session_id is not null)
);

comment on table sg_public.subject_version
  is 'Every version of the subjects. '
     'A subject is a collection of cards and other subjects. '
     'A subject has many cards and other subjects.';
comment on column sg_public.subject_version.version_id
  is 'The version ID -- a single subject can have many versions.';
comment on column sg_public.subject_version.created
  is 'When a user created this version.';
comment on column sg_public.subject_version.modified
  is 'When a user last modified this version.';
comment on column sg_public.subject_version.entity_id
  is 'The overall entity ID.';
comment on column sg_public.subject_version.previous_version_id
  is 'The previous version this version is based on.';
comment on column sg_public.subject_version.language
  is 'Which human language this subject contains.';
comment on constraint lang_check on sg_public.subject_version
  is 'Languages must be BCP47 compliant.';
comment on column sg_public.subject_version.name
  is 'The name of the subject.';
comment on column sg_public.subject_version.status
  is 'The status of the subject. The latest accepted version is current.';
comment on column sg_public.subject_version.available
  is 'Whether the subject is available to learners.';
comment on column sg_public.subject_version.tags
  is 'A list of tags. Think Bloom taxonomy.';
comment on column sg_public.subject_version.user_id
  is 'Which user created this version.';
comment on column sg_public.subject_version.session_id
  is 'If no user, which session created this version.';
comment on column sg_public.subject_version.body
  is 'The description of the goals of the subject.';
comment on constraint user_or_session on sg_public.subject_version
  is 'Ensure only the user or session has data.';

create table sg_public.subject_version_parent_child (
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  child_version_id uuid not null references sg_public.subject_version (version_id),
  parent_entity_id uuid not null references sg_public.subject_entity (entity_id),
  unique (child_version_id, parent_entity_id)
);

comment on table sg_public.subject_version_parent_child
  is 'A join table between a subject version and the parents.';
comment on column sg_public.subject_version_parent_child.id
  is 'The relationship ID.';
comment on column sg_public.subject_version_parent_child.created
  is 'When a user created this version.';
comment on column sg_public.subject_version_parent_child.modified
  is 'When a user last modified this version.';
comment on column sg_public.subject_version_parent_child.child_version_id
  is 'The version ID of the child subject.';
comment on column sg_public.subject_version_parent_child.parent_entity_id
  is 'The entity ID of the parent subject.';

create table sg_public.subject_version_before_after (
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  after_version_id uuid not null references sg_public.subject_version (version_id),
  before_entity_id uuid not null references sg_public.subject_entity (entity_id),
  unique (after_version_id, before_entity_id)
);

comment on table sg_public.subject_version_before_after
  is 'A join table between a subject version and the subjects before.';
comment on column sg_public.subject_version_before_after.id
  is 'The relationship ID.';
comment on column sg_public.subject_version_before_after.created
  is 'When a user created this version.';
comment on column sg_public.subject_version_before_after.modified
  is 'When a user last modified this version.';
comment on column sg_public.subject_version_before_after.after_version_id
  is 'The version ID of the after subject.';
comment on column sg_public.subject_version_before_after.before_entity_id
  is 'The entity ID of the before subject.';


create table sg_public.card_entity (
  entity_id uuid primary key references sg_public.entity (entity_id)
);

comment on table sg_public.card_entity
  is 'A list of all card entity IDs';
comment on column sg_public.card_entity.entity_id
  is 'The ID of the entity';

create table sg_public.card_version (
  -- all entity columns
  version_id uuid primary key references sg_public.entity_version (version_id),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  entity_id uuid not null references sg_public.card_entity (entity_id),
  previous_id uuid null references sg_public.card_version (version_id),
  language varchar(5) not null default 'en'
    constraint lang_check check (language ~* '^\w{2}(-\w{2})?$'),
  name text not null,
  status sg_public.entity_status not null default 'pending',
  available boolean not null default true,
  tags text[] null default array[]::text[],
  user_id uuid null references sg_public.user (id),
  session_id uuid null,
  -- and the rest....
  subject_id uuid not null references sg_public.subject_entity (entity_id),
  kind sg_public.card_kind not null,
  data jsonb not null,
  constraint user_or_session check (user_id is not null or session_id is not null),
  constraint valid_video_card check (
    kind <> 'video' or validate_json_schema($$ {
      "type": "object",
      "properties": {
        "site": {
          "type": "string",
          "enum": ["youtube", "vimeo"]
        },
        "video_id": { "type": "string" }
      },
      "required": ["site", "video_id"]
    } $$, data)
  ),
  constraint valid_page_card check (
    kind <> 'page' or validate_json_schema($$ {
      "type": "object",
      "properties": {
        "body": { "type": "string" }
      },
      "required": ["body"]
    } $$, data)
  ),
  constraint valid_unscored_embed_card check (
    kind <> 'unscored_embed' or validate_json_schema($$ {
      "type": "object",
      "properties": {
        "url": {
          "type": "string",
          "format": "uri"
        }
      },
      "required": ["url"]
    } $$, data)
  ),
  constraint valid_choice_card check (
    kind <> 'choice' or validate_json_schema($$ {
      "type": "object",
      "properties": {
        "body": {
          "type": "string"
        },
        "options": {
          "type": "object",
          "patternProperties": {
            "^[a-zA-Z0-9-]+$": {
              "type": "object",
              "properties": {
                "value": { "type": "string" },
                "correct": { "type": "boolean" },
                "feedback": { "type": "string" }
              },
              "required": ["value", "correct", "feedback"]
            }
          },
          "additionalProperties": false,
          "minProperties": 1
        },
        "max_options_to_show": {
          "type": "integer",
          "minimum": 2,
          "default": 4
        }
      },
      "required": ["body", "options", "max_options_to_show"]
    } $$, data)
  )
);

comment on table sg_public.card_version
  is 'Every version of the cards. A card is a single learning activity. '
     'A card belongs to a single subject.';
comment on column sg_public.card_version.version_id
  is 'The version ID -- a single card can have many versions.';
comment on column sg_public.card_version.created
  is 'When a user created this version.';
comment on column sg_public.card_version.modified
  is 'When a user last modified this version.';
comment on column sg_public.card_version.entity_id
  is 'The overall entity ID.';
comment on column sg_public.card_version.previous_id
  is 'The previous version this version is based on.';
comment on column sg_public.card_version.language
  is 'Which human language this card contains.';
comment on constraint lang_check on sg_public.card_version
  is 'Languages must be BCP47 compliant.';
comment on column sg_public.card_version.name
  is 'The name of the card.';
comment on column sg_public.card_version.status
  is 'The status of the card. The latest accepted version is current.';
comment on column sg_public.card_version.available
  is 'Whether the card is available to learners.';
comment on column sg_public.card_version.tags
  is 'A list of tags. Think Bloom taxonomy.';
comment on column sg_public.card_version.user_id
  is 'Which user created this version.';
comment on column sg_public.card_version.session_id
  is 'If no user, which session created this version.';
comment on column sg_public.card_version.subject_id
  is 'The subject the card belongs to.';
comment on column sg_public.card_version.kind
  is 'The subkind of the card, such as video or choice.';
comment on column sg_public.card_version.data
  is 'The data of the card. The card kind changes the data shape.';
comment on constraint valid_video_card on sg_public.card_version
  is 'If the `kind` is `video`, ensure `data` matches the data shape.';
comment on constraint valid_page_card on sg_public.card_version
  is 'If the `kind` is `page`, ensure `data` matches the data shape.';
comment on constraint valid_unscored_embed_card on sg_public.card_version
  is 'If the `kind` is `unscored_embed`, ensure `data` matches the data shape.';
comment on constraint valid_choice_card on sg_public.card_version
  is 'If the `kind` is `choice`, ensure `data` matches the data shape.';
comment on constraint user_or_session on sg_public.card_version
  is 'Ensure only the user or session has data.';

create trigger update_subject_version_modified
  before update on sg_public.subject_version
  for each row execute procedure sg_private.update_modified_column();
comment on trigger update_subject_version_modified on sg_public.subject_version
  is 'Whenever a subject version changes, update the `modified` column.';

create trigger update_subject_version_parent_child_modified
  before update on sg_public.subject_version_parent_child
  for each row execute procedure sg_private.update_modified_column();
comment on trigger update_subject_version_parent_child_modified
  on sg_public.subject_version_parent_child
  is 'Whenever a subject version changes, update the `modified` column.';

create trigger update_subject_version_before_after_modified
  before update on sg_public.subject_version_before_after
  for each row execute procedure sg_private.update_modified_column();
comment on trigger update_subject_version_before_after_modified
  on sg_public.subject_version_before_after
  is 'Whenever a subject version changes, update the `modified` column.';

create trigger update_card_version_modified
  before update on sg_public.card_version
  for each row execute procedure sg_private.update_modified_column();
comment on trigger update_card_version_modified on sg_public.card_version
  is 'Whenever a card version changes, update the `modified` column.';

create trigger insert_subject_version_user_or_session
  before insert on sg_public.subject_version
  for each row execute procedure sg_private.insert_user_or_session();
comment on trigger insert_subject_version_user_or_session
  on sg_public.subject_version
  is 'Automatically add the user_id or session_id.';

create trigger insert_card_version_user_or_session
  before insert on sg_public.card_version
  for each row execute procedure sg_private.insert_user_or_session();
comment on trigger insert_card_version_user_or_session
  on sg_public.card_version
  is 'Automatically add the user_id or session_id.';

create or replace function sg_public.new_subject(
  language varchar,
  name text,
  tags text[],
  body text,
  parent uuid[],
  before uuid[]
)
returns sg_public.subject_version as $$
  declare
    xentity_id uuid;
    xversion_id uuid;
    xsubject_version sg_public.subject_version;
  begin
    xentity_id := uuid_generate_v4();
    xversion_id := uuid_generate_v4();
    insert into sg_public.entity
    (entity_id, entity_kind) values (xentity_id, 'subject');
    insert into sg_public.subject_entity
    (entity_id) values (xentity_id);
    insert into sg_public.entity_version
    (version_id, entity_kind) values (xversion_id, 'subject');
    insert into sg_public.subject_version
    (version_id, entity_id, language, name, tags, body)
    values (xversion_id, xentity_id, language, name, tags, body)
    returning * into xsubject_version;
    insert into sg_public.subject_version_parent_child
    (child_version_id, parent_entity_id)
    select xversion_id, unnest(parent);
    insert into sg_public.subject_version_before_after
    (after_version_id, before_entity_id)
    select xversion_id, unnest(before);
    return xsubject_version;
  end;
$$ language plpgsql strict security definer;
comment on function sg_public.new_subject(
  varchar,
  text,
  text[],
  text,
  uuid[],
  uuid[]
) is 'Create a new subject.';
grant execute on function sg_public.new_subject(
  varchar,
  text,
  text[],
  text,
  uuid[],
  uuid[]
) to sg_anonymous, sg_user, sg_admin;

create or replace function sg_public.new_card(
  language varchar,
  name text,
  tags text[],
  subject_id uuid,
  kind sg_public.card_kind,
  data jsonb
)
returns sg_public.card_version as $$
  declare
    xentity_id uuid;
    xversion_id uuid;
    xcard_version sg_public.card_version;
  begin
    xentity_id := uuid_generate_v4();
    xversion_id := uuid_generate_v4();
    insert into sg_public.entity
    (entity_id, entity_kind) values (xentity_id, 'card');
    insert into sg_public.card_entity
    (entity_id) values (xentity_id);
    insert into sg_public.entity_version
    (version_id, entity_kind) values (xversion_id, 'card');
    insert into sg_public.card_version
    (version_id, entity_id, language, name, tags, subject_id, kind, data)
    values (xversion_id, xentity_id, language, name, tags, subject_id, kind, data)
    returning * into xcard_version;
    return xcard_version;
  end;
$$ language plpgsql strict security definer;
comment on function sg_public.new_card(
  varchar,
  text,
  text[],
  uuid,
  sg_public.card_kind,
  jsonb
) is 'Create a new card.';
grant execute on function sg_public.new_card(
  varchar,
  text,
  text[],
  uuid,
  sg_public.card_kind,
  jsonb
) to sg_anonymous, sg_user, sg_admin;

-- migrate:down

