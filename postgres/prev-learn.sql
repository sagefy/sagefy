-- migrate:up

create or replace function sg_private.insert_user_or_session()
returns trigger as $$
begin
  if (current_setting('jwt.claims.user_id')) then
    new.user_id = current_setting('jwt.claims.user_id')::uuid;
  end if;
  if (current_setting('jwt.claims.session_id')) then
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

create view sg_public.subject as
  select distinct on (entity_id) *
  from sg_public.subject_version
  where status = 'accepted'
  order by entity_id, created desc;
comment on view sg_public.subject
  is 'The latest accepted version of each subject.';

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
          "minimum": 0,
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

create view sg_public.card as
  select distinct on (entity_id) *
  from sg_public.card_version
  where status = 'accepted'
  order by entity_id, created desc;
comment on view sg_public.card
  is 'The latest accepted version of each card.';

grant select on table sg_public.subject_version
  to sg_anonymous, sg_user, sg_admin;
grant select on table sg_public.subject_version_before_after
  to sg_anonymous, sg_user, sg_admin;
grant select on table sg_public.subject_version_parent_child
  to sg_anonymous, sg_user, sg_admin;
grant select on table sg_public.card_version
  to sg_anonymous, sg_user, sg_admin;

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

create function sg_private.update_version_status()
returns trigger as $$
  declare
    role text;
  begin
    role := current_setting('jwt.claims.role')::text;
    if (role = 'sg_admin') then
      return new;
    end if;
    if (old.user_id <> current_setting('jwt.claims.user_id')) then
      raise exception 'A user may only change their own version status.'
        using errcode = '61C7AC84';
    end if;
    if (new.status <> 'declined') then
      raise exception 'A user may only change the version status to declined.'
        using errcode = '05F2D0E1';
    end if;
    if (old.status = 'accepted') then
      raise exception 'A user cannot change an accepted version.'
        using errcode = '62CF3D42';
    end if;
    return new;
  end;
$$ language plpgsql strict security definer;
comment on function sg_private.update_version_status()
  is 'A user may only change their own version status to declined.';
create trigger update_subject_version_status
  before update on sg_public.subject_version
  for each row execute procedure sg_private.update_version_status();
comment on trigger update_subject_version_status on sg_public.subject_version
  is 'A user may only decline their own un-accepted subject version.';
create trigger update_card_version_status
  before update on sg_public.card_version
  for each row execute procedure sg_private.update_version_status();
comment on trigger update_card_version_status on sg_public.card_version
  is 'A user may only decline their own un-accepted card version.';

create function sg_private.insert_subject_version_parent_child_cycle()
returns trigger as $$
  begin
    if exists(
      with recursive graph (entity_id, path, cycle) as (
        select
          sv.entity_id,
          array[sv.entity_id, new.entity_id],
          sv.entity_id = new.entity_id
        from sg_public.subject_version sv
        where new.version_id = sv.version_id
        union all
        select
          s.entity_id,
          g.path || s.entity_id,
          s.entity = any(g.path)
        from
          graph g,
          sg_public.subject_version_parent_child svpc,
          sg_public.subject s
        where
          g.entity_id = svpc.before_entity_id
          and svpc.version_id = s.version_id
          and not g.cycle
      )
      select *
    ) then
      raise exception 'Subject parent/child cannot form a cycle.'
        using errcode = '7876F332';
    else
      return new;
    end if;
  end;
$$ language plpgsql strict security definer;
create trigger insert_subject_version_parent_child_cycle
  before insert on sg_public.subject_version
  for each row execute procedure sg_private.insert_subject_version_parent_child_cycle();
comment on function sg_private.insert_subject_version_parent_child_cycle()
  is 'Ensure subject parent/child relations don''t form a cycle.';
comment on trigger insert_subject_version_parent_child_cycle
  on sg_public.subject_version
  is 'Ensure subject parent/child relations don''t form a cycle.';

create function sg_private.insert_subject_version_before_after_cycle()
returns trigger as $$
  begin
    if exists(
      with recursive graph (entity_id, path, cycle) as (
        select
          sv.entity_id,
          array[sv.entity_id, new.entity_id],
          sv.entity_id = new.entity_id
        from sg_public.subject_version sv
        where new.version_id = sv.version_id
        union all
        select
          s.entity_id,
          g.path || s.entity_id,
          s.entity = any(g.path)
        from
          graph g,
          sg_public.subject_version_before_after svba,
          sg_public.subject s
        where
          g.entity_id = svba.before_entity_id
          and svba.version_id = s.version_id
          and not g.cycle
      )
      select *
    ) then
      raise exception 'Subject before/after cannot form a cycle.'
        using errcode = 'D8182DC8';
    else
      return new;
    end if;
  end;
$$ language plpgsql strict security definer;
create trigger insert_subject_version_before_after_cycle
  before insert on sg_public.subject_version
  for each row execute procedure sg_private.insert_subject_version_before_after_cycle();
comment on function sg_private.insert_subject_version_before_after_cycle()
  is 'Ensure subject before/after relations don''t form a cycle.';
comment on trigger insert_subject_version_before_after_cycle
  on sg_public.subject_version
  is 'Ensure subject before/after relations don''t form a cycle.';

create function sg_public.new_subject(
  language varchar,
  name text,
  tags text[],
  body text,
  parent uuid[],
  before uuid[]
)
returns sg_public.subject_version as $$
  begin
    with entity as (
      insert into sg_public.entity
      (entity_kind) values ('subject')
    ),
    subject_entity as (
      insert into sg_public.subject_entity
      (entity_id) values (entity.entity_id)
    ),
    subject_version as (
      insert into sg_public.subject_version
      (entity_id, language, name, tags, body)
      values (entity.entity_id, language, name, tags, body)
    ),
    subject_parent as (
      insert into sg_public.subject_version_parent_child
      (child_version_id, parent_entity_id)
      values (subject_version.version_id, unnest(parent))
    )
    insert into sg_public.subject_version_before_after
    (after_version_id, before_entity_id)
    values (subject_version.version_id, unnest(before));
  end;
$$ language plpgsql;
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

create function sg_public.new_card(
  language varchar,
  name text,
  tags text[],
  subject_id uuid,
  kind text,
  data jsonb
)
returns sg_public.card_version as $$
  begin
    with entity as (
      insert into sg_public.entity
      (entity_kind) values ('card')
    ),
    card_entity as (
      insert into sg_public.card_entity
      (entity_id) values (entity.entity_id)
    )
    insert into sg_public.card_version
    (entity_id, language, name, tags, subject_id, kind, data)
    values (entity.entity_id, language, name, tags, subject_id, kind, data);
  end;
$$ language plpgsql;
comment on function sg_public.new_card(
  varchar,
  text,
  text[],
  uuid,
  text,
  jsonb
) is 'Create a new card.';
grant execute on function sg_public.new_card(
  varchar,
  text,
  text[],
  uuid,
  text,
  jsonb
) to sg_anonymous, sg_user, sg_admin;

create or replace function sg_public.search_subjects(query text)
returns setof sg_public.subject as $$
  with documents as (
    select
      entity_id,
      to_tsvector('english', unaccent(name)) ||
      to_tsvector('english', unaccent(array_to_string(tags, ' '))) ||
      to_tsvector('english', unaccent(body)) as document
    from sg_public.subject
  ),
  ranking as (
    select
      s.entity_id as entity_id,
      ts_rank(d.document, websearch_to_tsquery('english', unaccent(query))) as rank
    from
      sg_public.subject s,
      documents d
    where
      d.document @@ websearch_to_tsquery('english', unaccent(query))
      and s.entity_id = d.entity_id
    order by rank desc
  )
  select s.*
  from
    ranking r,
    sg_public.subject s
  where
    s.entity_id = r.entity_id
  order by r.rank desc;
$$ language sql stable;
comment on function sg_public.search_subjects(text)
  is 'Search subjects.';
grant execute on function sg_public.search_subjects(text)
  to sg_anonymous, sg_user, sg_admin;

create table sg_public.user_subject (
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  user_id uuid null references sg_public.user (id) on delete cascade,
  session_id uuid null,
  subject_id uuid not null references sg_public.subject_entity (entity_id),
  unique (user_id, subject_id),
  unique (session_id, subject_id),
  constraint user_or_session check (user_id is not null or session_id is not null)
);

comment on table sg_public.user_subject
  is 'The association between a user and a subject. '
     'This is a subject the learner is learning.';
comment on column sg_public.user_subject.id
  is 'The ID of the user subject.';
comment on column sg_public.user_subject.created
  is 'When the user created the association.';
comment on column sg_public.user_subject.modified
  is 'When the association last changed.';
comment on column sg_public.user_subject.user_id
  is 'Which user the association belongs to.';
comment on column sg_public.user_subject.session_id
  is 'If not user, the session the association belongs to.';
comment on column sg_public.user_subject.subject_id
  is 'Which subject the association belongs to.';
comment on constraint user_or_session on sg_public.user_subject
  is 'Ensure only the user or session has data.';

create table sg_public.response (
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  user_id uuid null references sg_public.user (id),
  session_id uuid null,
  card_id uuid not null references sg_public.card_entity (entity_id),
  subject_id uuid not null references sg_public.subject_entity (entity_id),
  response text not null,
  score real not null check (score >= 0 and score <= 1),
  learned real not null check (score >= 0 and score <= 1),
  constraint user_or_session check (user_id is not null or session_id is not null)
);

comment on table sg_public.response
  is 'When a learner responds to a card, we record the result.';
comment on column sg_public.response.id
  is 'The ID of the response.';
comment on column sg_public.response.created
  is 'When the user created the response.';
comment on column sg_public.response.modified
  is 'When the system last modified the response.';
comment on column sg_public.response.user_id
  is 'The user the response belongs to.';
comment on column sg_public.response.session_id
  is 'If not user, the session_id the response belongs to.';
comment on column sg_public.response.card_id
  is 'The card (entity id) that the response belongs to.';
comment on column sg_public.response.subject_id
  is 'The subject (entity id) that the response belongs to... '
     'at the time of the response';
comment on column sg_public.response.response
  is 'How the user responded.';
comment on column sg_public.response.score
  is 'The score, 0->1, of the response.';
comment on column sg_public.response.learned
  is 'The estimated probability the learner has learned the subject, '
     'after this response.';
comment on constraint user_or_session on sg_public.response
  is 'Ensure only the user or session has data.';

create trigger insert_user_subject_user_or_session
  before insert on sg_public.user_subject
  for each row execute procedure sg_private.insert_user_or_session();
comment on trigger insert_user_subject_user_or_session
  on sg_public.user_subject
  is 'Whenever I make a new user subject, auto fill the `user_id` column';

create trigger insert_response_user_or_session
  before insert on sg_public.response
  for each row execute procedure sg_private.insert_user_or_session();
comment on trigger insert_response_user_or_session
  on sg_public.response
  is 'Whenever I make a new response, auto fill the `user_id` column';

create trigger update_user_subject_modified
  before update on sg_public.user_subject
  for each row execute procedure sg_private.update_modified_column();
comment on trigger update_user_subject_modified on sg_public.user_subject
  is 'Whenever a user subject changes, update the `modified` column.';

create trigger update_response_modified
  before update on sg_public.response
  for each row execute procedure sg_private.update_modified_column();
comment on trigger update_response_modified on sg_public.response
  is 'Whenever a response changes, update the `modified` column.';

create function sg_public.select_latest_response(subject_id uuid)
returns sg_public.response as $$
  -- If no response yet, default to 0.4
  select *
  from sg_public.response
  where sg_public.response.subject_id = subject_id and (
    user_id = current_setting('jwt.claims.user_id')::uuid
    or session_id = current_setting('jwt.claims.session_id')::uuid
  )
  order by created desc
  limit 1;
$$ language sql stable;
comment on function sg_public.select_latest_response(uuid)
  is 'Get the latest response from the user on the given subject.';

create or replace function sg_private.score_response()
returns trigger as $$
  declare
    card sg_public.card;
    prior sg_public.response;
    prior_learned real := 0.4;
    option jsonb;
    score real;
    learned real;
    slip constant real := 0.1;
    guess constant real := 0.3;
    transit constant real := 0.05;
  begin
    -- Overall: Fill in (subject_id, score, learned)
    -- Validate if the response to the card is valid.
    card := (
      select *
      from sg_public.card
      where sg_public.card.entity_id = new.card_id
      limit 1
    );
    if (!card) then
      raise exception 'No card found.' using errcode = 'EE05C989';
    end if;
    if (card.kind <> 'choice') then -- scored kinds only
      raise exception 'You may only respond to a scored card.'
        using errcode = '1306BF1C';
    end if;
    option := card.data->'options'->new.response;
    if (!option) then
      raise exception 'You must submit an available response `id`.'
        using errcode = '681942FD';
    end if;
    -- Set default values
    new.subject_id := card.subject_id;
    -- Score the response
    new.score := case when option->'correct' then 1 else 0 end;
    -- Calculate p(learned)
    prior := sg_public.select_latest_response(card.subject_id);
    if (prior) then
      prior_learned := prior.learned;
    end if;
    learned := (
      new.score * (
        (prior_learned * (1 - slip)) /
        (prior_learned * (1 - slip) + (1 - prior_learned) * guess)
      ) +
      (1 - new.score) * (
        (prior_learned * slip) /
        (prior_learned * slip + (1 - prior_learned) * (1 - guess))
      )
    );
    new.learned := learned + (1 - learned) * transit;
    return new;
  end;
$$ language plpgsql strict security definer;
comment on function sg_private.score_response()
  is 'After I respond to a card, score the result and update model.';

create trigger insert_response_score
  before insert on sg_public.response
  for each row execute procedure sg_private.score_response();
comment on trigger insert_response_score on sg_public.response
  is 'After I respond to a card, score the result and update model.';

-- Enable RLS.
alter table sg_public.user_subject enable row level security;
alter table sg_public.response enable row level security;

create function sg_public.select_popular_subjects()
returns setof sg_public.subject as $$
  select *
  from sg_public.subject
  order by (
    select count(*)
    from sg_public.user_subject
    where subject_id = entity_id
  )
  limit 5;
$$ language sql stable;
comment on function sg_public.select_popular_subjects()
  is 'Select the 5 most popular subjects.';
grant execute on function sg_public.select_popular_subjects()
  to sg_anonymous, sg_user, sg_admin;

-- Select usubj: user or admin self or with setting.
grant select on table sg_public.user_subject to sg_user, sg_admin;
create policy select_user_subject on sg_public.user_subject
  for select to sg_user, sg_admin
  using (user_id = current_setting('jwt.claims.user_id')::uuid);
comment on policy select_user_subject on sg_public.user_subject
  is 'A user or admin may select their own subject relationships.';

-- Insert usubj: user or admin.
grant insert (subject_id) on table sg_public.user_subject to sg_user, sg_admin;
create policy insert_user_subject on sg_public.user_subject
  for insert to sg_user, sg_admin;
comment on policy insert_user_subject on sg_public.user_subject
  is 'A user or admin may insert a user subject relationship.';

-- Update usubj: none.

-- Delete usubj: user or admin self.
grant delete on table sg_public.user_subject to sg_user, sg_admin;
create policy delete_user_subject on sg_public.user_subject
  for delete to sg_user, sg_admin
  using (user_id = current_setting('jwt.claims.user_id')::uuid);
comment on policy delete_user_subject on sg_public.user_subject
  is 'A user or admin can delete their own user subject.';

-- Select response: any self.
grant select on table sg_public.response to sg_anonymous, sg_user, sg_admin;
create policy select_response on sg_public.response
  for select to sg_anonymous, sg_user, sg_admin
  using (
    user_id = current_setting('jwt.claims.user_id')::uuid
    or session_id = current_setting('jwt.claims.session_id')::uuid
  );
comment on policy select_response on sg_public.response
  is 'Anyone may select their own responses.';

-- Insert response: any via function.
grant insert (card_id, response)
  on table sg_public.response to sg_anonymous, sg_user, sg_admin;
create policy insert_response on sg_public.response
  for insert to sg_anonymous, sg_user, sg_admin;
comment on policy insert_response on sg_public.response
  is 'Anyone may insert `card_id` and `response` into responses.';

-- Update & delete response: none.

create function sg_public.select_card_to_learn(subject_id uuid)
returns sg_public.card as $$
  declare
    latest_response sg_public.response;
    kinds text[];
  begin
    -- What is p(learned) currently for the subject?
    latest_response := (select sg_public.select_latest_response(subject_id));
    -- Decide on a scored or unscored type
    kinds := (
      select case when random() > (
        0.5 + 0.5 * (latest_response.learned or 0.4)
      ) then
        array['choice'] -- scored kinds
      else
        array['video', 'page', 'unscored_embed'] -- unscored kinds
      end
    );
    select *
    from sg_public.card
    where sg_public.card.subject_id = subject_id
      and sg_public.card.kind = any(kinds)
      -- Don't allow the previous card as the next card
      and sg_public.card.entity_id <> latest_response.card_id
    -- Select cards of kind at random
    order by random()
    limit 1;
  end;
  -- Future version: When estimating parameters and the card kind is scored,
  -- prefer 0.25 < correct < 0.75
$$ language plpgsql strict security definer;
comment on function sg_public.select_card_to_learn(uuid)
  is 'After I select a subject, search for a suitable card.';
grant execute on function sg_public.select_card_to_learn(uuid)
  to sg_anonymous, sg_user, sg_admin;

create or replace function sg_public.select_subject_to_learn(subject_id uuid)
returns sg_public.subject as $$
  -- determine all child subjects graph
  with recursive children_graph (version_id, entity_id, path) as (
    select
      s.version_id,
      s.entity_id,
      array[s.entity_id]
    from
      sg_public.subject s
    where
      s.entity_id = subject_id
    union all
    select
      s.version_id,
      s.entity_id,
      cg.path || s.entity_id
    from
      children_graph cg,
      sg_public.subject s,
      sg_public.subject_version_parent_child svpc
    where
      cg.version_id = svpc.child_version_id
      and svpc.parent_entity_id = s.entity_id
  ),
  -- only keep those with direct cards
  filtered as (
    select cg.*, (
      select count(*)
      from sg_public.card c
      where c.subject_id = cg.entity_id
    ) as card_count
    from children_graph cg
    -- where card_count > 0
  ),
  -- count the depth -- how many subjects after this one
  before_graph (version_id, entity_id, path) as (
    select
      s.version_id,
      s.entity_id,
      array[s.entity_id]
    from filtered s
    union all
    select
      s.version_id,
      s.entity_id,
      bg.path || s.entity_id
    from
      before_graph bg,
      sg_public.subject_version_before_after svba,
      sg_public.subject s
    where
      bg.version_id = svba.after_version_id
      and svba.before_entity_id = s.entity_id
  ),
  -- cut inaccessibile subjects -- haven't learned a before > 0.99
  allowed as (
    select *
    from
      before_graph bg
    where (
      select count((
        select r.learned
        from sg_public.select_latest_response(entity_id) r
      ) > 0.99)
      from unnest(bg.path) as entity_id
    ) = array_length(bg.path, 1)
  )
  -- limit 5
  select s.*
  from
    allowed a,
    sg_public.subject s
  where
    a.version_id = s.version_id
  order by
    array_length(a.path, 1) desc
  limit 5;
$$ language sql stable;
comment on function sg_public.select_subject_to_learn(uuid)
  is 'After I select a main subject, search for suitable child subjects.';
grant execute on function sg_public.select_subject_to_learn(uuid)
  to sg_anonymous, sg_user, sg_admin;

-- migrate:down

