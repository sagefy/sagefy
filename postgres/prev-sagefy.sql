------ Generic > Trigger Functions ---------------------------------------------

create or replace function sg_private.insert_user_id_column()
returns trigger as $$
begin new.user_id = current_setting('jwt.claims.user_id')::uuid;
  return new;
  -- TODO update to store either user_id or session_id
end;
$$ language 'plpgsql';
comment on function sg_private.insert_user_id_column()
  is 'When inserting a row, automatically set the `user_id` field.';








------ Users > Functions -------------------------------------------------------

create function sg_public.user_md5_email(user sg_public.user)
returns text as $$
  select md5(lower(trim(email)))
  from sg_private.user
  where user_id = user.id
  limit 1;
$$ language sql stable;
comment on function sg_public.user_md5_email(sg_public.user)
  is 'The user''s email address as an MD5 hash, for Gravatars. '
     'See https://bit.ly/2F6cR0M';
grant execute on function sg_public.user_md5_email(sg_public.user)
  to sg_anonymous, sg_user, sg_admin;













------ Cards, Units, Subjects --------------------------------------------------

------ Cards, Units, Subjects > Types ------------------------------------------

create type sg_public.entity_kind as enum(
  'card',
  'unit',
  'subject'
);
comment on type sg_public.entity_kind
  is 'The three types of entities.';

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

------ Cards, Units, Subjects > Tables -----------------------------------------

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

create table sg_public.unit_entity (
  entity_id uuid primary key references sg_public.entity (entity_id)
);

comment on table sg_public.unit_entity
  is 'A list of all unit entity IDs.';
comment on column sg_public.unit_entity.entity_id
  is 'The ID of the entity.';

create table sg_public.unit_version (
  -- all entity columns
  version_id uuid primary key references sg_public.entity_version (version_id),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  entity_id uuid not null references sg_public.unit_entity (entity_id),
  previous_id uuid null references sg_public.unit_version (version_id),
  language varchar(5) not null default 'en'
    constraint lang_check check (language ~* '^\w{2}(-\w{2})?$'),
  name text not null,
  status sg_public.entity_status not null default 'pending',
  available boolean not null default true,
  tags text[] null default array[]::text[],
  user_id uuid null references sg_public.user (id),
  -- and the rest....
  body text not null
  -- also see join table: sg_public.unit_version_require
);

comment on table sg_public.unit_version
  is 'Every version of the units. A unit is a single learning goal. '
     'A unit has many cards and can belong to many subjects.';
comment on column sg_public.unit_version.version_id
  is 'The version ID -- a single unit can have many versions.';
comment on column sg_public.unit_version.created
  is 'When a user created this version.';
comment on column sg_public.unit_version.modified
  is 'When a user last modified this version.';
comment on column sg_public.unit_version.entity_id
  is 'The overall entity ID.';
comment on column sg_public.unit_version.previous_id
  is 'The previous version this version is based on.';
comment on column sg_public.unit_version.language
  is 'Which human language this unit contains.';
comment on constraint lang_check on sg_public.unit_version
  is 'Languages must be BCP47 compliant.';
comment on column sg_public.unit_version.name
  is 'The name of the unit.';
comment on column sg_public.unit_version.status
  is 'The status of the unit. The latest accepted version is current.';
comment on column sg_public.unit_version.available
  is 'Whether the unit is available to learners.';
comment on column sg_public.unit_version.tags
  is 'A list of tags. Think Bloom taxonomy.';
comment on column sg_public.unit_version.user_id
  is 'Which user created this version.';
comment on column sg_public.unit_version.body
  is 'The description of the goal of the unit.';

create table sg_public.unit_version_require (
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  version_id uuid not null references sg_public.unit_version (version_id),
  require_id uuid not null references sg_public.unit_entity (entity_id),
  unique (version_id, require_id)
);

comment on table sg_public.unit_version_require
  is 'A join table between a unit version and the units it requires.';
comment on column sg_public.unit_version_require.id
  is 'The relationship ID.';
comment on column sg_public.unit_version_require.created
  is 'When a user created this version.';
comment on column sg_public.unit_version_require.modified
  is 'When a user last modified this version.';
comment on column sg_public.unit_version_require.version_id
  is 'The version ID.';
comment on column sg_public.unit_version_require.require_id
  is 'The entity ID of the required unit.';

create view sg_public.unit as
  select distinct on (entity_id) *
  from sg_public.unit_version
  where status = 'accepted'
  order by entity_id, created desc;
comment on view sg_public.unit
  is 'The latest accepted version of each unit.';

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
  previous_id uuid null references sg_public.subject_version (version_id),
  language varchar(5) not null default 'en'
    constraint lang_check check (language ~* '^\w{2}(-\w{2})?$'),
  name text not null,
  status sg_public.entity_status not null default 'pending',
  available boolean not null default true,
  tags text[] null default array[]::text[],
  user_id uuid null references sg_public.user (id),
  -- and the rest....
  body text not null
  -- also see join table: sg_public.subject_version_member
);

comment on table sg_public.subject_version
  is 'Every version of the subjects. '
     'A subject is a collection of units and other subjects. '
     'A subject has many units and other subjects.';
comment on column sg_public.subject_version.version_id
  is 'The version ID -- a single subject can have many versions.';
comment on column sg_public.subject_version.created
  is 'When a user created this version.';
comment on column sg_public.subject_version.modified
  is 'When a user last modified this version.';
comment on column sg_public.subject_version.entity_id
  is 'The overall entity ID.';
comment on column sg_public.subject_version.previous_id
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
comment on column sg_public.subject_version.body
  is 'The description of the goals of the subject.';

create table sg_public.subject_version_member (
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  version_id uuid not null references sg_public.subject_version (version_id),
  entity_id uuid not null,
  entity_kind sg_public.entity_kind not null,
  foreign key (entity_id, entity_kind)
    references sg_public.entity (entity_id, entity_kind),
  unique (version_id, entity_id),
  check (entity_kind = 'unit' or entity_kind = 'subject')
);

comment on table sg_public.subject_version_member
  is 'A join table between a subject version and '
     'its member units and subjects.';
comment on column sg_public.subject_version_member.id
  is 'The relationship ID.';
comment on column sg_public.subject_version_member.created
  is 'When a user created this version.';
comment on column sg_public.subject_version_member.modified
  is 'When a user last modified this version.';
comment on column sg_public.subject_version_member.version_id
  is 'The subject version ID.';
comment on column sg_public.subject_version_member.entity_id
  is 'The entity ID of the member.';
comment on column sg_public.subject_version_member.entity_kind
  is 'The entity kind of the member.';

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
  -- and the rest....
  unit_id uuid not null references sg_public.unit_entity (entity_id),
  kind sg_public.card_kind not null,
  data jsonb not null,
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
            "^[a-zA-Z0-9\-]+$": {
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
  ),
);

comment on table sg_public.card_version
  is 'Every version of the cards. A card is a single learning activity. '
     'A card belongs to a single unit.';
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
comment on column sg_public.card_version.unit_id
  is 'The unit the card belongs to.';
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

create view sg_public.card as
  select distinct on (entity_id) *
  from sg_public.card_version
  where status = 'accepted'
  order by entity_id, created desc;
comment on view sg_public.card
  is 'The latest accepted version of each card.';

------ Cards, Units, Subjects > Indexes ----------------------------------------

------ Cards, Units, Subjects > Functions --------------------------------------

create function sg_private.insert_unit_version_cycle()
returns trigger as $$
  if exists(
    with recursive graph (entity_id, path, cycle) as (
      select uv.entity_id,
        array(uv.entity_id, new.entity_id),
        uv.entity_id = new.entity_id
      from sg_public.unit_version uv
      where new.version_id = uv.version_id
      union all
      select u.entity_id,
        g.path || u.entity_id,
        u.entity_id = any(g.path)
      from graph g, sg_public.unit_version_require uvr, sg_public.unit u
      where g.entity_id = uvr.entity_id
        and uvr.version_id = u.version_id
        and not g.cycle
    )
    select *
  ) then
    raise exception 'Unit requires cannot form a cycle.'
      using errcode = '7876F332';
  else
    return new;
  end if;
$$ language 'plpgsql';
comment on function sg_private.insert_unit_version_cycle()
  is 'Ensure units do not form a cycle of requires.';

create function sg_private.insert_subject_version_cycle()
returns trigger as $$
  if exists(
    recursive graph (parent_id, path, cycle) as (
      select sv.entity_id,
        array(sv.entity_id, new.entity_id),
        sv.entity_id = new.entity_id
      from sg_public.subject_version sv
      where new.version_id = sv.version_id and new.entity_kind = 'subject'
      union all
      select s.entity_id,
        g.path || s.entity_id,
        s.entity_id = any(g.path)
      from graph g, sg_public.subject_version_member svm, sg_public.subject s
      where g.entity_id = svm.entity_id
        and svm.entity_kind = 'subject'
        and svm.version_id = s.version_id
        and not g.cycle
    )
    select *
  ) then
    raise exception 'Subject members cannot form a cycle.'
      using errcode = '1318F849';
  else
    return new;
  end if;
$$ language 'plpgsql';
comment on function sg_private.insert_unit_version_cycle()
  is 'Ensure subjects do not form a cycle of members.';

create function sg_private.insert_version_notice()
returns trigger as $$
  insert into sg_public.notice
  (user_id, kind, entity_kind, entity_id)
  select (
    unnest(
      select distinct user_id
      from sg_public.follow
      where new.entity_id = sg_public.follow.entity_id
    ),
    'version_pending',
    replace(tg_table_name, '_version', ''),
    new.entity_id
  );
$$ language 'plpgsql';
comment on function sg_private.insert_version_notice()
  is 'After I insert a new version, notify followers.';

create function sg_private.update_version_status()
returns trigger as $$
  declare
    role text;
  begin
    role := current_setting('jwt.claims.role')::text;
    if (role = 'sg_admin') return new;
    if (old.user_id <> current_setting('jwt.claims.user_id') then
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
$$ language 'plpgsql';
comment on function sg_private.update_version_status()
  is 'A user may only change their own version status to declined.';

create function sg_private.update_version_notice()
returns trigger as $$
  if (new.status <> old.status) then
    insert into sg_public.notice
    (user_id, kind, entity_kind, entity_id)
    select (
      unnest(
        select distinct user_id
        from sg_public.follow
        where new.entity_id = sg_public.follow.entity_id
      ),
      'version_' || new.status,
      replace(tg_table_name, '_version', ''),
      new.entity_id
    );
  end if;
$$ language 'plpgsql';
comment on function sg_private.update_version_notice()
  is 'After I update a version status, notify followers.';

create function sg_public.search_units(query text)
returns setof sg_public.unit as $$
  select
    *,
    to_tsvector('english', unaccent(name)) ||
    to_tsvector('english', unaccent(tags)) ||
    to_tsvector('english', unaccent(body)) as document,
    ts_rank(document, websearch_to_tsquery('english', unaccent(query))) as rank
  from sg_public.unit
  where document @@ websearch_to_tsquery('english', unaccent(query))
  order by rank desc;
$$ language sql;
comment on function sg_public.search_units(text)
  is 'Search units.';

create function sg_public.search_subjects(query text)
returns setof sg_public.subject as $$
  select
    *,
    to_tsvector('english', unaccent(name)) ||
    to_tsvector('english', unaccent(tags)) ||
    to_tsvector('english', unaccent(body)) as document,
    ts_rank(document, websearch_to_tsquery('english', unaccent(query))) as rank
  from sg_public.subject
  where document @@ websearch_to_tsquery('english', unaccent(query))
  order by rank desc;
$$ language sql;
comment on function sg_public.search_subjects(text)
  is 'Search subjects.';

create function sg_public.search_cards(query text)
returns setof sg_public.card as $$
  select
    *,
    to_tsvector('english', unaccent(name)) ||
    to_tsvector('english', unaccent(tags)) ||
    to_tsvector('english', unaccent(data)) as document,
    ts_rank(document, websearch_to_tsquery('english', unaccent(query))) as rank
  from sg_public.card
  where document @@ websearch_to_tsquery('english', unaccent(query))
  order by rank desc;
$$ language sql;
comment on function sg_public.search_cards(text)
  is 'Search cards.';

create function sg_public.search_entities(query text)
returns setof (entity_id, name, body, kind) as $$
  select entity_id, name, body, 'subject' as kind
  from sg_public.search_subjects(query)
  union all
  select entity_id, name, body, 'unit' as kind
  from sg_public.search_units(query)
  union all
  select entity_id, name, data as body, 'card' as kind
  from sg_public.search_cards(query)
  order by rank desc;
$$ language sql;
comment on function sg_public.search_entities(text)
  is 'Search subject, units, and cards.';

create function sg_public.select_units_by_subject(subject_id uuid)
returns setof sg_public.unit as $$
  with latest_subject_member as (
    select s.entity_id as parent_id,
      m.entity_id as child_id,
      m.entity_kind as child_kind
    from sg_public.subject s, sg_public.subject_version_member m
    where m.version_id = s.version_id
  ),
  recursive child_subject (entity_id) as (
    select child_id as entity_id
    from latest_subject_member
    where child_kind = 'subject' and parent_id = subject_id
    union all
    select l.child_id as entity_id
    from latest_subject_member l, child_subject c
    where l.child_kind = 'subject' and c.child_id = l.parent_id
  ),
  child_unit as (
    select child_id as entity_id
    from latest_subject_member
    where child_kind = 'unit' and (
      parent_id = subject_id
      or parent_id in child_subject
    )
  )
  select u.*
  from sg_public.unit u
  where u.entity_id in child_unit;
$$ language sql stable;
comment on function sg_public.select_units_by_subject(uuid)
  is 'Select recursively all child units of a subject.';

create function sg_public.select_subjects_by_unit(unit_id uuid)
returns setof sg_public.subject as $$
  with latest_subject_member as (
    select s.entity_id as parent_id,
      m.entity_id as child_id,
      m.entity_kind as child_kind
    from sg_public.subject s, sg_public.subject_version_member m
    where m.version_id = s.version_id
  ),
  recursive parent_subject (entity_id) as (
    select parent_id as entity_id
    from latest_subject_member
    where child_kind = 'unit' and child_id = unit_id
    union all
    select l.parent_id as entity_id
    from latest_subject_member l, parent_subject p
    where l.child_kind = 'subject' and p.parent_id = l.child_id
  ),
  select s.*
  from sg_public.subject s, parent_subject m
  where m.entity_id = s.entity_id;
$$ language sql stable;
comment on function sg_public.select_subjects_by_unit(uuid)
  is 'Select recursively all parent subjects of a unit.';

create function sg_public.unit_depth(unit_id uuid, all_unit sg_public.unit)
returns int as $$
  with latest_require as (
    select as r.require_id as left_id,
       u.entity_id as right_id
    from all_unit u, sg_public.unit_version_require r
    where r.version_id = u.version_id
  ),
  recursive depth_calc as (
    select *
    from latest_require
    where right_id = unit_id
    union all
    select *
    from latest_require l, depth_calc d
    where l.right_id = d.left_id
  )
  select count(depth_calc);
$$ language sql stable;
comment on sg_public.unit_depth(uuid, sg_public.unit)
  is 'Calculate the depth of a unit in a require graph.';

create function sg_public.select_popular_subjects()
returns setof sg_public.subject as $$
  select *, (
    select count(*)
    from sg_public.user_subject
    where subject_id = entity_id
  ) as user_count
  from sg_public.subject
  order by user_count
  limit 10;
$$ language sql stable;
comment on function sg_public.select_popular_subjects()
  is 'Select the 10 most popular subjects.';

create function sg_public.select_my_cards()
returns setof sg_public.card as $$
  select *
  from sg_public.card
  where entity_id in (
    select entity_id
    from sg_public.card_version
    where user_id = current_setting('jwt.claims.user_id')::uuid
  );
$$ language sql stable;
comment on function sg_public.select_my_cards()
  is 'Select cards I created or worked on.';

create function sg_public.select_my_units()
returns setof sg_public.unit as $$
  select *
  from sg_public.unit
  where entity_id in (
    select entity_id
    from sg_public.unit_version
    where user_id = current_setting('jwt.claims.user_id')::uuid
  );
$$ language sql stable;
comment on function sg_public.select_my_units()
  is 'Select units I created or worked on.';

create function sg_public.select_my_subjects()
returns setof sg_public.subject as $$
  select *
  from sg_public.subject
  where entity_id in (
    select entity_id
    from sg_public.subject_version
    where user_id = current_setting('jwt.claims.user_id')::uuid
  );
$$ language sql stable;
comment on function sg_public.select_my_subjects()
  is 'Select subjects I created or worked on.';

create function sg_public.new_unit(
  language varchar,
  name text,
  tags text[],
  body text,
  require_ids uuid[]
)
returns sg_public.unit_version as $$
  with entity as (
    insert into sg_public.entity
    (entity_kind) values ('unit')
  ),
  unit_entity as (
    insert into sg_public.unit_entity
    (entity_id) values (entity.entity_id)
  ),
  unit_version as (
    insert into sg_public.unit_version
    (entity_id, language, name, tags, body, user_id)
    values (entity.entity_id, language, tags, body,
      current_setting('jwt.claims.user_id')::uuid)
  )
  insert into sg.unit_version_require
  (version_id, require_id)
  select (unit_version.version_id, unnest(require_ids));
$$ language 'plpgsql' volatile;
comment on function sg_public.new_unit(
  varchar,
  text,
  text[],
  text,
  uuid[]
) is 'Create a new card.';

create function sg_public.edit_unit(
  entity_id uuid,
  name text,
  tags text[],
  body text,
  require_ids uuid[]
)
returns sg_public.unit_version as $$
  with previous as (
    select *
    from sg_public.unit
    where sg_public.unit.entity_id = entity_id
    limit 1
  ),
  with unit_version as (
    insert into sg_public.unit_version
    (entity_id, previous_id, name, tags, body, user_id)
    values (entity_id, previous.version_id, name, tags, body,
      current_setting('jwt.claims.user_id')::uuid)
  )
  insert into sg.unit_version_require
  (version_id, require_id)
  select (unit_version.version_id, unnest(require_ids));
$$ language 'plpgsql' volatile;
comment on function sg_public.edit_unit(
  uuid,
  text,
  text[],
  text,
  uuid[]
) is 'Edit an existing unit.';

create function sg_public.new_subject(
  language varchar,
  name text,
  tags text[],
  body text,
  members jsonb
)
returns sg_public.subject_version as $$
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
    (entity_id, language, name, tags, body, user_id)
    values (entity.entity_id, language, name, tags, body,
      current_setting('jwt.claims.user_id')::uuid)
  )
  insert into sg_public.subject_version_member
  (version_id, entity_id, entity_kind)
  select (subject_version.version_id,
    json_array_elements(members) as (entity_id, entity_kind));
$$ language 'plpgsql' volatile;
comment on function sg_public.new_subject(
  varchar,
  text,
  text[],
  text,
  jsonb
) is 'Create a new subject.';

create function sg_public.edit_subject(
  entity_id uuid
  name text,
  tags text[],
  body text,
  members jsonb
)
returns sg_public.subject_version as $$
  with previous as (
    select *
    from sg_public.subject
    where sg_public.subject.entity_id = entity_id
    limit 1
  ),
  subject_version as (
    insert into sg_public.subject_version
    (entity_id, previous_id, name, tags, body, user_id)
    values (entity_id, previous.version_id, name, tags, body,
      current_setting('jwt.claims.user_id')::uuid)
  )
  insert into sg_public.subject_version_member
  (version_id, entity_id, entity_kind)
  select (subject_version.version_id,
    json_array_elements(members) as (entity_id, entity_kind));
$$ language 'plpgsql' volatile;
comment on function sg_public.edit_subject(
  uuid
  text,
  text[],
  text,
  jsonb
) is 'Edit an existing subject.';

create function sg_public.new_card(
  language varchar,
  name text,
  tags text[],
  unit_id uuid,
  kind text,
  data jsonb
)
returns sg_public.card_version as $$
  with entity as (
    insert into sg_public.entity
    (entity_kind) values ('card')
  ),
  card_entity as (
    insert into sg_public.card_entity
    (entity_id) values (entity.entity_id)
  ),
  insert into sg_public.card_version
  (entity_id, language, name, tags, unit_id, kind, data, user_id)
  values (entity.entity_id, language, name, tags, unit_id,
    kind, data, current_setting('jwt.claims.user_id')::uuid);
$$ language 'plpgsql' volatile;
comment on function sg_public.new_card(
  varchar,
  text,
  text[],
  uuid,
  text,
  jsonb
) is 'Create a new card.';

create function sg_public.edit_card(
  entity_id uuid,
  name text,
  tags text[],
  unit_id uuid,
  kind text
  data jsonb
)
returns sg_public.card_version as $$
  with previous as (
    select *
    from sg_public.card
    where sg_public.card.entity_id = entity_id
    limit 1
  )
  insert into sg_public.card_version
  (entity_id, previous_id, name, tags, unit_id, kind, data, user_id)
  values (entity_id, previous.version_id, name, tags, unit_id, kind, data,
    current_setting('jwt.claims.user_id')::uuid);
$$ language 'plpgsql' volatile;
comment on function sg_public.edit_card(
  uuid,
  text,
  text[],
  uuid,
  text
  jsonb
) is 'Edit an existing card.';

------ Cards, Units, Subjects > Triggers ---------------------------------------

create trigger insert_unit_version_cycle
  before insert on sg_public.unit_version_require
  for each row execute procedure sg_private.insert_unit_version_cycle();
comment on trigger insert_unit_version_cycle on sg_public.unit_version_require
  is 'Ensure units do not form a cycle of requires.';

create trigger insert_subject_version_cycle
  before insert on sg_public.subject_version_member
  for each row execute procedure sg_private.insert_subject_version_cycle();
comment on trigger insert_subject_version_cycle
  on sg_public.subject_version_member
  is 'Ensure subject do not form a cycle of members.';

create trigger insert_unit_version_notice
  after insert on sg_public.unit_version
  for each row execute procedure sg_private.insert_version_notice();
comment on trigger insert_unit_version_notice on sg_public.unit_version
  is 'After I insert a new unit version, notify followers.';

create trigger insert_subject_version_notice
  after insert on sg_public.subject_version
  for each row execute procedure sg_private.insert_version_notice();
comment on trigger insert_subject_version_notice on sg_public.subject_version
  is 'After I insert a new subject version, notify followers.';

create trigger insert_card_version_notice
  after insert on sg_public.card_version
  for each row execute procedure sg_private.insert_version_notice();
comment on trigger insert_card_version_notice on sg_public.card_version
  is 'After I insert a new card version, notify followers.';

create trigger update_unit_version_modified
  before update on sg_public.unit_version
  for each row execute procedure sg_private.update_modified_column();
comment on trigger update_unit_version_modified on sg_public.unit_version
  is 'Whenever a unit version changes, update the `modified` column.';

create trigger update_unit_version_status
  before update on sg_public.unit_version
  for each row execute procedure sg_private.update_version_status()
comment on trigger update_unit_version_status on sg_public.unit_version
  is 'A user may only decline their own un-accepted unit version.';

create trigger update_unit_version_notice
  after update on sg_public.unit_version
  for each row execute procedure sg_private.update_version_notice();
comment on trigger update_unit_version_notice on sg_public.unit_version
  is 'After I update a unit version, notify followers.';

create trigger update_unit_version_require_modified
  before update on sg_public.unit_version_require
  for each row execute procedure sg_private.update_modified_column();
comment on trigger update_unit_version_require_modified
  on sg_public.unit_version_require
  is 'Whenever a unit version require changes, update the `modified` column.';

create trigger update_subject_version_modified
  before update on sg_public.subject_version
  for each row execute procedure sg_private.update_modified_column();
comment on trigger update_subject_version_modified on sg_public.subject_version
  is 'Whenever a subject version changes, update the `modified` column.';

create trigger update_subject_version_status
  before update on sg_public.subject_version
  for each row execute procedure sg_private.update_version_status()
comment on trigger update_subject_version_status on sg_public.subject_version
  is 'A user may only decline their own un-accepted subject version.';

create trigger update_subject_version_notice
  after update on sg_public.subject_version
  for each row execute procedure sg_private.update_version_notice();
comment on trigger update_subject_version_notice on sg_public.subject_version
  is 'After I update a subject version, notify followers.';

create trigger update_subject_version_member_modified
  before update on sg_public.subject_version_member
  for each row execute procedure sg_private.update_modified_column();
comment on trigger update_subject_version_member_modified
  on sg_public.subject_version_member
  is 'Whenever a subject version member changes, update the `modified` column.';

create trigger update_card_version_modified
  before update on sg_public.card_version
  for each row execute procedure sg_private.update_modified_column();
comment on trigger update_card_version_modified on sg_public.card_version
  is 'Whenever a card version changes, update the `modified` column.';

create trigger update_card_version_status
  before update on sg_public.card_version
  for each row execute procedure sg_private.update_version_status()
comment on trigger update_card_version_status on sg_public.card_version
  is 'A user may only decline their own un-accepted card version.';

create trigger update_card_version_notice
  after update on sg_public.card_version
  for each row execute procedure sg_private.update_version_notice();
comment on trigger update_card_version_notice on sg_public.card_version
  is 'After I update a card version, notify followers.';

------ Cards, Units, Subjects > Permissions ------------------------------------

-- Select card, unit, subject: any.
grant select on table sg_public.unit_version
  to sg_anonymous, sg_user, sg_admin;
grant select on table sg_public.unit_version_require
  to sg_anonymous, sg_user, sg_admin;
grant select on table sg_public.subject_version
  to sg_anonymous, sg_user, sg_admin;
grant select on table sg_public.subject_version_member
  to sg_anonymous, sg_user, sg_admin;
grant select on table sg_public.card_version
  to sg_anonymous, sg_user, sg_admin;

-- Insert (or new version) card, unit, subject: any via function.
grant execute on function sg_public.new_unit(
  varchar,
  text,
  text[],
  text,
  uuid[]
) to sg_anonymous, sg_user, sg_admin;
grant execute on function sg_public.edit_unit(
  uuid,
  text,
  text[],
  text,
  uuid[]
) to sg_anonymous, sg_user, sg_admin;
grant execute on function sg_public.new_subject(
  varchar,
  text,
  text[],
  text,
  jsonb
) to sg_anonymous, sg_user, sg_admin;
grant execute on function sg_public.edit_subject(
  uuid
  text,
  text[],
  text,
  jsonb
) to sg_anonymous, sg_user, sg_admin;
grant execute on function sg_public.new_card(
  varchar,
  text,
  text[],
  uuid,
  text,
  jsonb
) to sg_anonymous, sg_user, sg_admin;
grant execute on function sg_public.edit_card(
  uuid,
  text,
  text[],
  uuid,
  text
  jsonb
) to sg_anonymous, sg_user, sg_admin;

-- Update & delete card, unit, subject: admin.
grant update, delete on table sg_public.unit_version to sg_admin;
grant update (status) on table sg_public.unit_version to sg_user;
grant update, delete on table sg_public.unit_version_require to sg_admin;
grant update, delete on table sg_public.subject_version to sg_admin;
grant update (status) on table sg_public.subject_version to sg_user;
grant update, delete on table sg_public.subject_version_member to sg_admin;
grant update, delete on table sg_public.card_version to sg_admin;
grant update (status) on table sg_public.card_version to sg_user;

grant execute on function sg_public.select_popular_subjects()
  to sg_anonymous, sg_user, sg_admin;

grant execute on function sg_public.select_my_cards()
  to sg_user, sg_admin;
grant execute on function sg_public.select_my_units()
  to sg_user, sg_admin;
grant execute on function sg_public.select_my_subjects()
  to sg_user, sg_admin;

grant execute on function sg_public.select_units_by_subject(uuid)
  to sg_anonymous, sg_user, sg_admin;
grant execute on function sg_public.select_subjects_by_unit(uuid)
  to sg_anonymous, sg_user, sg_admin;

grant execute on function sg_public.search_unit(text)
  to sg_anonymous, sg_user, sg_admin;
grant execute on function sg_public.search_subject(text)
  to sg_anonymous, sg_user, sg_admin;
grant execute on function sg_public.search_cart(text)
  to sg_anonymous, sg_user, sg_admin;
grant execute on function sg_public.search_entity(text)
  to sg_anonymous, sg_user, sg_admin;
















------ Topics & Posts ----------------------------------------------------------

------ Topics & Posts > Types --------------------------------------------------

create type sg_public.post_kind as enum(
  'post',
  'proposal',
  'vote'
);
comment on type sg_public.post_kind
  is 'The three kinds of posts.';

------ Topics & Posts > Tables -------------------------------------------------

create table sg_public.topic (
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  user_id uuid null references sg_public.user (id),
  name text not null,
  entity_id uuid not null,
  entity_kind sg_public.entity_kind not null,
  foreign key (entity_id, entity_kind)
    references sg_public.entity (entity_id, entity_kind)
);

comment on table sg_public.topic
  is 'The topics on an entity''s talk page.';
comment on column sg_public.id
  is 'The public ID of the topic.';
comment on column sg_public.created
  is 'When the user created the topic.';
comment on column sg_public.modified
  is 'When the user last modified the topic.';
comment on column sg_public.user_id
  is 'The user who created the topic.';
comment on column sg_public.entity_id
  is 'The entity the topic belongs to.';
comment on column sg_public.entity_kind
  is 'The kind of entity the topic belongs to.';

create table sg_public.post (
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  user_id uuid null references sg_public.user (id)
    check (kind <> 'vote' or user_id is not null),
  topic_id uuid not null references sg_public.topic (id),
  kind sg_public.post_kind not null default 'post',
  body text null
    check (kind = 'vote' or body is not null),
  parent_id uuid null references sg_public.post (id)
    check (kind <> 'vote' or parent_id is not null),
  response boolean null
    check (kind <> 'vote' or response is not null)
  -- also see join table: sg_public.post_entity_version
  -- specific to kind = 'proposal'
);

comment on table sg_public.post
  is 'The posts on an entity''s talk page. Belongs to a topic.';
comment on column sg_public.post.id
  is 'The ID of the post.';
comment on column sg_public.post.created
  is 'When the user created the post.';
comment on column sg_public.post.modified
  is 'When the post last changed.';
comment on column sg_public.post.user_id
  is 'The user who created the post.';
comment on column sg_public.post.topic_id
  is 'The topic the post belongs to.';
comment on column sg_public.post.kind
  is 'The kind of post (post, proposal, vote).';
comment on column sg_public.post.body
  is 'The body or main content of the post.';
comment on column sg_public.post.parent_id
  is 'If the post is a reply, which post it replies to.';
comment on column sg_public.post.response
  is 'If the post is a vote, yes/no on approving.';

create table sg_public.post_entity_version (
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  post_id uuid not null references sg_public.post (id),
  version_id uuid not null,
  entity_kind sg_public.entity_kind not null,
  foreign key (version_id, entity_kind)
    references sg_public.entity_version (version_id, entity_kind)
  unique (post_id, version_id)
);

comment on table sg_public.post_entity_version
  is 'A join table between a proposal (post) and its entity versions.';
comment on column sg_public.post_entity_version.id
  is 'The relationship ID.';
comment on column sg_public.post_entity_version.created
  is 'When a user created this post.';
comment on column sg_public.post_entity_version.modified
  is 'When a user last modified this post.';
comment on column sg_public.post_entity_version.post_id
  is 'The post ID.';
comment on column sg_public.post_entity_version.version_id
  is 'The entity ID of the entity version.';

------ Topics & Posts > Indexes ------------------------------------------------

create unique index post_vote_unique_idx
  on sg_public.post (user_id, parent_id)
  where kind = 'vote';
comment on index post_vote_unique_idx
  is 'A user may only vote once on a proposal.';

------ Topics & Posts > Functions ----------------------------------------------

create function sg_private.verify_post()
returns trigger as $$
  declare
    parent sg_public.post;
  begin
    if (new.parent_id) then
      parent := (
        select *
        from sg_public.post
        where id = new.parent_id
      );
      if (parent.topic_id <> new.topic_id) then
        raise exception 'A reply must belong to the same topic.'
          using errcode = '76177573';
      end if;
      if (new.kind = 'vote' and parent.kind <> 'proposal') then
        raise exception 'A vote may only reply to a proposal.'
          using errcode = '8DF72C56';
      end if;
      if (new.kind = 'vote' and parent.user_id = new.user_id) then
        raise exception 'A user cannot vote on their own proposal.'
          using errcode = 'E47E0411';
      end if;
    end if;
  end;
$$ language 'plpgsql';
comment on function sg_private.verify_post()
  is 'Verify valid data when creating or updating a post.';

create function sg_private.insert_topic_notice()
returns trigger as $$
  insert into sg_public.notice
  (user_id, kind, entity_kind, entity_id)
  select (
    unnest(
      select distinct user_id
      from sg_public.follow
      where new.entity_id = sg_public.follow.entity_id
    ),
    'insert_topic',
    new.entity_kind,
    new.entity_id
  );
$$ language 'plpgsql';
comment on function sg_private.insert_topic_notice()
  is 'After I insert a new topic, notify followers.';

create function sg_private.insert_post_notice()
returns trigger as $$
  declare
    topic sg_public.topic;
  begin
    topic := (
      select *
      from sg_public.topic
      where id = new.topic_id
      limit 1;
    );
    insert into sg_public.notice
    (user_id, kind, entity_kind, entity_id)
    select (
      unnest(
        select distinct user_id
        from sg_public.follow
        where topic.entity_id = sg_public.follow.entity_id
      ),
      'insert_post',
      topic.entity_kind,
      topic.entity_id
    );
  end;
$$ language 'plpgsql';
comment on function sg_private.insert_post_notice()
  is 'After I insert a new post, notify followers.';

create function sg_private.follow_own_topic()
returns trigger as $$
  insert into sg_public.follow
  (entity_id, entity_kind)
  values
  (new.entity_id, new.entity_kind)
  on conflict do nothing;
$$ language 'plpgsql';
comment on function sg_private.follow_own_topic()
  is 'When I create a topic, I follow the entity.';

create function sg_private.follow_own_post()
returns trigger as $$
  declare
    topic sg_public.topic;
  begin
    topic := (
      select *
      from sg_public.topic
      where id = new.topic_id
      limit 1;
    );
    insert into sg_public.follow
    (entity_id, entity_kind)
    values
    (topic.entity_id, topic.entity_kind)
    on conflict do nothing;
    end;
$$ language 'plpgsql';
comment on function sg_private.follow_own_post()
  is 'When I create a post, I follow the entity.';

create function sg_private.vote_to_status()
returns trigger as $$
  if new.kind <> 'proposal' and new.kind <> 'vote' then
    return new;
  end if;
  if old and (old.status = 'accepted' or old.status = 'declined') then
    return new;
  end if;
  if new.response = false then
    return new;
  end if;
  -- For now, just accept
  update sg_public.unit_version
  set status = 'accepted'
  where version_id in (
    select version_id
    from sg_public.post_entity_version
    where post_id = new.id
      and entity_kind = 'unit'
  );
  update sg_public.card_version
  set status = 'accepted'
  where version_id in (
    select version_id
    from sg_public.post_entity_version
    where post_id = new.id
      and entity_kind = 'card'
  );
  update sg_public.subject_version
  set status = 'accepted'
  where version_id in (
    select version_id
    from sg_public.post_entity_version
    where post_id = new.id
      and entity_kind = 'subject'
  );
  -- Later version:
  -- get all the users who voted on the proposal
  -- count the number of accepted versions total per user: points
  -- assign a score of 0->1 (non-linear) to each user: 1 - e ^ (-points / 40) (computed column?)
  -- determine the number of learners impacted (computed column?)
  -- -- for a subject, get all subjects upward + current, then sum the user_subject counts
  -- -- for a unit, get all the subjects upward, then sum the user_subject counts
  -- -- for a card, get the unit, then unit procedure
  -- if numLearners > 0 and sum(noVotes) > log100(numLearners), change the status to blocked
  -- if sum(yesVotes) > log5(numLearners), change the status to accepted
  -- else, change the status to pending
$$ language 'plpgsql';
comment on function sg_private.vote_to_status()
  is 'When a new proposal or vote happens, change entity status if possible';

------ Topics & Posts > Triggers -----------------------------------------------

create trigger insert_topic_user_id
  before insert on sg_public.topic
  for each row execute procedure sg_private.insert_user_id_column();
comment on trigger insert_topic_user_id on sg_public.topic
  is 'Whenever I make a new topic, auto fill the `user_id` column';

create trigger insert_topic_notice
  after insert on sg_public.topic
  for each row execute procedure sg_private.insert_topic_notice();
comment on trigger insert_topic_notice on sg_public.topic
  is 'After I insert a new topic, notify followers.'

create trigger insert_post_user_id
  before insert on sg_public.post
  for each row execute procedure sg_private.insert_user_id_column();
comment on trigger insert_post_user_id on sg_public.post
  is 'Whenever I make a new post, auto fill the `user_id` column';

create trigger insert_post_verify
  before insert on sg_public.post
  for each row execute procedure sg_private.verify_post();
comment on trigger insert_post_verify on sg_public.post
  is 'Whenever I make a new post, check that the post is valid.';

create trigger insert_post_notice
  after insert on sg_public.post
  for each row execute procedure sg_private.insert_post_notice();
comment on trigger insert_post_notice on sg_public.post
  is 'After I insert a new post, notify followers.';

create trigger update_topic_modified
  before update on sg_public.topic
  for each row execute procedure sg_private.update_modified_column();
comment on trigger update_topic_modified on sg_public.topic
  is 'Whenever a topic changes, update the `modified` column.';

create trigger update_post_modified
  before update on sg_public.post
  for each row execute procedure sg_private.update_modified_column();
comment on trigger update_post_modified on sg_public.post
  is 'Whenever a post changes, update the `modified` column.';

create trigger update_post_verify
  before update on sg_public.post
  for each row execute procedure sg_private.verify_post();
comment on trigger update_post_verify on sg_public.post
  is 'Whenever I make a new post, check that the post is valid.';

create trigger update_post_entity_version_modified
  before update on sg_public.post_entity_version
  for each row execute procedure sg_private.update_modified_column();
comment on trigger update_post_entity_version_modified
  on sg_public.post_entity_version
  is 'Whenever a post entity version changes, update the `modified` column.';

create trigger vote_to_status
  after insert, update on sg_public.post
  for each row execute sg_private.vote_to_status();
comment on trigger vote_to_status
  on sg_public.post
  is 'When a new proposal or vote happens, change entity status if possible';

create trigger follow_own_topic
  after insert on sg_public.topic
  for each row execute procedure sg_private.follow_own_topic();
comment on trigger follow_own_topic on sg_public.topic
  is 'When I create a topic, I follow the entity.';

create trigger follow_own_post
  after insert on sg_public.post
  for each row execute procedure sg_private.follow_own_post();
comment on trigger follow_own_post on sg_public.post
  is 'When I create a post, I follow the entity.';

------ Topics & Posts > Permissions --------------------------------------------

-- Enable RLS.
alter table sg_public.topic enable row level security;
alter table sg_public.post enable row level security;

-- Select topic: any.
grant select on table sg_public.topic to sg_anonymous, sg_user, sg_admin;
create policy select_topic on sg_public.topic
  for select -- any user
  using (true);
comment on policy select_topic on sg_public.topic
  is 'Anyone can select topics.';

-- Insert topic: any.
grant insert (name, entity_id, entity_kind) on table sg_public.topic
  to sg_anonymous, sg_user, sg_admin;
create policy insert_topic on sg_public.topic
  for insert (name, entity_id, entity_kind) -- any user
  using (true);

-- Update topic: user self (name), or admin.
grant update (name) on table sg_public.topic to sg_user;
grant update on table sg_public.topic to sg_admin;
create policy update_topic on sg_public.topic
  for update (name) to sg_user
  using (user_id = current_setting('jwt.claims.user_id')::uuid);
comment on policy update_topic on sg_public.topic
  is 'A user can update the name of their own topic.';
create policy update_topic_admin on sg_public.topic
  for update to sg_admin
  using (true);
comment on policy update_topic on sg_public.topic
  is 'An admin can update the name of any topic.';

-- Delete topic: admin.
grant delete on table sg_public.topic to sg_admin;
create policy delete_topic_admin on sg_public.topic
  for delete to sg_admin
  using (true);
comment on policy delete_topic_admin on sg_public.topic
  is 'An admin can delete any topic.';

-- Select post: any.
grant select on table sg_public.post to sg_anonymous, sg_user, sg_admin;
create policy select_post on sg_public.post
  for select -- any user
  using (true);
comment on policy select_post on sg_public.post
  is 'Anyone can select posts.';

-- Insert post: any.
grant insert (topic_id, kind, body, parent_id, response) on table sg_public.post
  to sg_anonymous, sg_user, sg_admin;
create policy insert_post on sg_public.post
  for insert (topic_id, kind, body, parent_id, response) -- any user
  using (true);

-- Update post: user self (body, response), or admin.
grant update (body, response) on table sg_public.post to sg_user;
grant update on table sg_public.post to sg_admin;
create policy update_post on sg_public.post
  for update (body, response) to sg_user
  using (user_id = current_setting('jwt.claims.user_id')::uuid);
comment on policy update_post on sg_public.post
  is 'A user can update the body or response of their own post.';
create policy update_post_admin on sg_public.post
  for update to sg_admin
  using (true);
comment on policy update_post_admin on sg_public.post
  is 'An admin can update any post.';

-- Delete post: admin.
grant delete on table sg_public.post to sg_admin;
create policy delete_post_admin on sg_public.post
  for delete to sg_admin
  using (true);
comment on policy delete_post_admin on sg_public.post
  is 'An admin can delete any post.';

-- Select post_entity_version: any.
grant select on table sg_public.post_entity_version
  to sg_anonymous, sg_user, sg_admin;

-- Insert post_entity_version, see function above.

-- Update or delete post_entity_version: admin.
grant update, delete on table sg_public.post_entity_version
  to sg_admin;














------ Notices & Follows -------------------------------------------------------

------ Notices & Follows > Types -----------------------------------------------

create type sg_public.notice_kind as enum(
  'version_pending',
  'version_blocked',
  'version_declined',
  'version_accepted',
  'insert_topic',
  'insert_post'
);
comment on type sg_public.notice_kind
  is 'The kinds of notices. Expanding.';

------ Notices & Follows > Tables ----------------------------------------------

create table sg_public.notice (
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  user_id uuid not null references sg_public.user (id) on delete cascade,
  read boolean not null default false,
  kind sg_public.notice_kind not null,
  entity_id uuid not null,
  entity_kind sg_public.entity_kind not null,
  foreign key (entity_id, entity_kind)
    references sg_public.entity (entity_id, entity_kind)
);

comment on table sg_public.notice
  is 'A notice is a message that an entity has recent activity.';
comment on column table sg_public.notice.id
  is 'The ID of the notice.';
comment on column table sg_public.notice.created
  is 'When the system created the notice.';
comment on column table sg_public.notice.modified
  is 'When the notice last changed.';
comment on column table sg_public.notice.user_id
  is 'Which user the notice belongs to.';
comment on column table sg_public.notice.kind
  is 'The kind of notice.';
comment on column sg_public.notice.entity_id
  is 'The entity the notice informs.';
comment on column sg_public.notice.entity_kind
  is 'The kind of entity notice informs.';
comment on column table sg_public.notice.read
  is 'Whether or not the user has read the notice.';

create table sg_public.follow (
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  user_id uuid not null references sg_public.user (id) on delete cascade,
  entity_id uuid not null,
  entity_kind sg_public.entity_kind not null,
  unique (user_id, entity_id),
  foreign key (entity_id, entity_kind)
    references sg_public.entity (entity_id, entity_kind)
);

comment on table sg_public.follow
  is 'A follow is an association between a user and an entity. '
     'The user indicates they want notices for the entity.'
comment on column sg_public.follow.id
  is 'The ID of the follow.';
comment on column sg_public.follow.created
  is 'When the user or system created the follow.';
comment on column sg_public.follow.modified
  is 'When the user or system modified the follow.';
comment on column sg_public.follow.user_id
  is 'The user the follow belongs to.';
comment on column sg_public.follow.entity_id
  is 'The entity the follow belongs to.';
comment on column sg_public.follow.entity_kind
  is 'The kind of entity the follow belongs to.';

------ Notices & Follows > Indexes ---------------------------------------------

------ Notices & Follows > Functions -------------------------------------------

------ Notices & Follows > Triggers --------------------------------------------

create trigger insert_follow_user_id
  before insert on sg_public.follow
  for each row execute procedure sg_private.insert_user_id_column();
comment on trigger insert_follow_user_id on sg_public.follow
  is 'Whenever I make a new follow, auto fill the `user_id` column';

create trigger update_notice_modified
  before update on sg_public.notice
  for each row execute procedure sg_private.update_modified_column();
comment on trigger update_notice_modified on sg_public.notice
  is 'Whenever a notice changes, update the `modified` column.';

create trigger update_follow_modified
  before update on sg_public.follow
  for each row execute procedure sg_private.update_modified_column();
comment on trigger update_follow_modified on sg_public.follow
  is 'Whenever a follow changes, update the `modified` column.';

------ Notices & Follows > Permissions -----------------------------------------

-- Enable RLS.
alter table sg_public.notice enable row level security;
alter table sg_public.follow enable row level security;

-- Select follow: user or admin self.
grant select on table sg_public.follow to sg_user, sg_admin;
create policy select_follow on sg_public.follow
  for select to sg_user, sg_admin
  using (user_id = current_setting('jwt.claims.user_id')::uuid);
comment on policy select_follow on sg_public.follow
  is 'A user or admin can select their own follows.';

-- Insert follow: user or admin.
grant insert (entity_id, entity_kind) on table sg_public.follow
  to sg_user, sg_admin;
create policy insert_follow on sg_public.follow
  for insert (entity_id, entity_kind) to sg_user, sg_admin
  user (true);

-- Update follow: none.

-- Delete follow: user or admin self.
grant delete on table sg_public.follow to sg_user, sg_admin;
create policy delete_follow on sg_public.follow
  for select to sg_user, sg_admin
  using (user_id = current_setting('jwt.claims.user_id')::uuid);
comment on policy delete_follow on sg_public.follow
  is 'A user or admin can delete their own follows.';

-- Select notice: user or admin self.
grant select on table sg_public.notice to sg_user, sg_admin;
create policy select_notice on sg_public.notice
  for select to sg_user, sg_admin
  using (user_id = current_setting('jwt.claims.user_id')::uuid);
comment on policy select_notice on sg_public.notice
  is 'A user or admin can select their own notices.';

-- Insert notice: none.

-- Update notice: user or admin self (read).
grant update on table sg_public.notice to sg_user, sg_admin;
create policy update_notice on sg_public.notice
  for update (read) to sg_user, sg_admin
  using (user_id = current_setting('jwt.claims.user_id')::uuid);
comment on policy update_notice on sg_public.notice
  is 'A user or admin can mark a notice as read or unread.';

-- Delete notice: user or admin self.
grant delete on table sg_public.notice to sg_user, sg_admin;
create policy delete_notice on sg_public.notice
  for delete to sg_user, sg_admin
  using (user_id = current_setting('jwt.claims.user_id')::uuid);
comment on policy delete_notice on sg_public.notice
  is 'A user or admin can delete their own notices.';


















------ User Subjects, Responses ------------------------------------------------

------ User Subjects, Responses > Types ----------------------------------------

------ User Subjects, Responses > Tables ---------------------------------------

create table sg_public.user_subject (
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  user_id uuid not null references sg_public.user (id) on delete cascade,
  subject_id uuid not null references sg_public.subject_entity (entity_id),
  unique (user_id, subject_id)
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
comment on column sg_public.user_subject.subject_id
  is 'Which subject the association belongs to.';

create table sg_public.response (
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  user_id uuid null references sg_public.user (id),
  session_id uuid null,
  card_id uuid not null references sg_public.card_entity (entity_id),
  unit_id uuid not null references sg_public.unit_entity (entity_id),
  response text not null,
  score real not null check (score >= 0 and score <= 1),
  learned real not null check (score >= 0 and score <= 1),
  check (user_id is not null or session_id is not null)
);

comment on table sg_public.response
  is 'When a learner responds to a card, we record the result.';
comment on table sg_public.response.id
  is 'The ID of the response.';
comment on table sg_public.response.created
  is 'When the user created the response.';
comment on table sg_public.response.modified
  is 'When the system last modified the response.';
comment on table sg_public.response.user_id
  is 'The user the response belongs to.';
comment on table sg_public.response.card_id
  is 'The card (entity id) that the response belongs to.';
comment on table sg_public.response.unit_id
  is 'The unit (entity id) that the response belongs to... '
     'at the time of the response';
comment on table sg_public.response.response
  is 'How the user responded.';
comment on table sg_public.response.score
  is 'The score, 0->1, of the response.';
comment on table sg_public.response.learned
  is 'The estimated probability the learner has learned the unit, '
     'after this response.';

------ User Subjects, Responses > Indexes --------------------------------------

------ User Subjects, Responses > Functions ------------------------------------

create function sg_public.select_latest_response(unit_id uuid)
returns sg_public.response as $$
  -- If no response yet, default to 0.4
  select
    sg_public.response.* as *,
    case when count(*) > 0 then sg_public.response.learned else 0.4 end as learned
  from sg_public.response
  where sg_public.response.unit_id = unit_id and (
    current_setting('jwt.claims.role')::text <> 'sg_anonymous'
    and user_id = current_setting('jwt.claims.user_id')::uuid
  ) or (
    current_setting('jwt.claims.role')::text = 'sg_anonymous'
    and session_id = current_setting('jwt.claims.session_id')::uuid
  )
  order by created desc
  limit 1;
$$ language sql stable;
comment on function sg_public.select_latest_response(uuid)
  is 'Get the latest response from the user on the given unit.';

create function sg_public.select_unit_to_learn(subject_id uuid)
returns setof sg_public.unit as $$
  select all_unit.* as *,
    sg_public.select_latest_response(all_unit.entity_id).learned as learned,
    sg_public.unit_depth(all_unit.unit_id, all_unit) as depth
  from sg_public.select_units_by_subject(subject_id) as all_unit
  where learned < 0.99
  order by depth desc
  limit 5;
$$ language sql stable;
comment on function sg_public.select_unit_to_learn(uuid)
  is 'After I select a subject, recommend up to 5 units to choose from.';

create function sg_public.select_card_to_learn(unit_id uuid)
returns sg_public.card as $$
  -- What is p(learned) currently for the unit?
  with latest_response as (
    select sg_public.select_latest_response(unit_id)
  ),
  -- Decide on a scored or unscored type
  kinds as (
    select case when rand() > 0.5 + 0.5 * latest_response.learned then
      ('choice') -- scored kinds
    else
      ('video', 'page', 'unscored_embed') -- unscored kinds
    end
  ),
  -- Select cards of kind at random
  -- Don't allow the previous card as the next card
  select *
  from sg_public.card
  where sg_public.card.unit_id = unit_id
    and kind in kinds
    and entity_id <> latest_response.card_id
  order by random()
  limit 1;
  -- Future version: When estimating parameters and the card kind is scored,
  -- prefer 0.25 < correct < 0.75
$$ language sql volatile;
comment on function sg_public.select_card_to_learn(uuid)
  is 'After I select a unit, search for a suitable card.';

create function sg_private.score_response()
returns trigger as $$
  declare
    card sg_public.card;
    prior sg_public.response;
    option jsonb;
    score real;
    learned real;
    slip constant real := 0.1;
    guess constant real := 0.3;
    transit constant real := 0.05;
  begin
    -- Overall: Fill in (user_id, session_id, unit_id, score, learned)
    -- Validate if the response to the card is valid.
    card := (
      select *
      from sg_public.card
      where sg_public.card.entity_id = new.card_id
      limit 1;
    )
    if (!card) then
      raise exception 'No card found.' with errcode = 'EE05C989';
    end if;
    if (card.kind <> 'choice') then -- scored kinds only
      raise exception 'You may only respond to a scored card.'
        with errcode = '1306BF1C';
    end if;
    option := card.data->'options'->new.response;
    if (!option) then
      raise exception 'You must submit an available response `id`.'
        with errcode = '681942FD';
    end if;
    -- Set default values
    new.user_id := current_setting('jwt.claims.user_id')::uuid;
    new.session_id := current_setting('jwt.claims.session_id')::uuid;
    new.unit_id := card.unit_id;
    -- Score the response
    new.score := case when option->'correct' then 1 else 0 end;
    -- Calculate p(learned)
    prior := sg_public.select_latest_response(card.unit_id);
    learned := (
      new.score * (
        (prior.learned * (1 - slip)) /
        (prior.learned * (1 - slip) + (1 - prior.learned) * guess)
      ) +
      (1 - new.score) * (
        (prior.learned * slip) /
        (prior.learned * slip + (1 - prior.learned) * (1 - guess))
      )
    );
    new.learned := learned + (1 - learned) * transit;
    return new;
  end;
$$ language 'plpgsql';
comment on function sg_private.score_response()
  is 'After I respond to a card, score the result and update model.';

------ User Subjects, Responses > Triggers -------------------------------------

create trigger insert_user_subject_user_id
  before insert on sg_public.user_subject
  for each row execute procedure sg_private.insert_user_id_column();
comment on trigger insert_user_subject_user_id on sg_public.user_subject
  is 'Whenever I make a new user subject, auto fill the `user_id` column';

create trigger insert_response_score
  before insert on sg_public.response
  for each row execute procedure sg_private.score_response();
comment on trigger insert_response_score on sg_public.response
  is 'After I respond to a card, score the result and update model.';

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

------ User Subjects, Responses > Permissions ----------------------------------

-- Enable RLS.
alter table sg_public.user_subject enable row level security;
alter table sg_public.response enable row level security;

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
  for insert (subject_id) to sg_user, sg_admin
  using (true);
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
create policy select_response to sg_public.response
  for select to sg_anonymous, sg_user, sg_admin
  using ((
    current_setting('jwt.claims.role')::text <> 'sg_anonymous'
    and user_id = current_setting('jwt.claims.user_id')::uuid
  ) or (
    current_setting('jwt.claims.role')::text = 'sg_anonymous'
    and session_id = current_setting('jwt.claims.session_id')::uuid
  ));
comment on policy select_response to sg_public.response
  is 'Anyone may select their own responses.';

-- Insert response: any via function.
grant insert (card_id, response)
  on table sg_public.response to sg_anonymous, sg_user, sg_admin;
create policy insert_response to sg_public.response
  for insert (card_id, response) to sg_anonymous, sg_user, sg_admin
  user (true);
comment on policy insert_response to sg_public.response
  is 'Anyone may insert `card_id` and `response` into responses.'

-- Update & delete response: none.

grant execute on function sg_public.select_unit_to_learn(uuid)
  to sg_anonymous, sg_user, sg_admin;
grant execute on function sg_public.select_card_to_learn(uuid)
  to sg_anonymous, sg_user, sg_admin;














