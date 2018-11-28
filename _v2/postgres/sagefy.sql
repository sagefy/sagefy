-- This file should be kept up-to-date as the latest, current version.

-- ENSURE UTF-8

create extension if not exists "uuid-ossp";
create extension if not exists "pgcrypto";

---- Generic > Schemas and Roles

create schema sg_public; -- Exposed to GraphQL
create schema sg_hidden; -- Not exposed to GraphQL
create schema sg_private; -- Secrets
-- todo comment

create role sg_postgraphile login password 'xyz'; -- todo !!! fix password
create role sg_user;
create role sg_anonymous;
grant sg_user to sg_postgraphile;
grant sg_anonymous to sg_postgraphile;
-- todo comment on roles

---- Generic > Trigger Functions

create or replace function sg_private.update_modified_column()
returns trigger as $$
begin new.modified = now();
  return new;
end;
$$ language 'plpgsql';
-- todo comment


------ Users -------------------------------------------------------------------

------ Users > Types -----------------------------------------------------------

create type sg_public.email_frequency as enum(
  'immediate', 'daily', 'weekly', 'never'
);

------ Users > Tables ----------------------------------------------------------

create table sg_public.user (
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  name text not null unique,
  view_subjects boolean not null default false
);

-- TODO comment table and columns, constraints

create table sg_private.user (
  user_id uuid primary key references sg_public.user (id) on delete cascade,
  email text not null unique
    constraint email_check check (email ~* '^\S+@\S+\.\S+$'),
  password varchar(60) not null
    constraint pass_check check (password ~* '^\$2\w\$.*$'),
  email_frequency sg_public.email_frequency not null default 'immediate'
);

-- TODO comment table and columns, constraints

------ Users > Validations (TODO) ----------------------------------------------

------ Users > Sessions (TODO) -------------------------------------------------

create function sg_public.sign_up(
  name text,
  email text,
  password text,
) returns sg_public.user as $$
declare
  user sg_public.user
begin
  insert into sg_public.user (name) values (name)
    returning * as user;
  insert into sg_private.user (user_id, email, password)
    values (user.id, email, crypt(password, gen_salt('bf', 8)));
  return user;
end;
$$ language plpgsql strict security definer;
comment on function sg_public.sign_up(text, text, text)
  is 'Signs up a single user.';

create type sg_public.jwt_token as (
  role text,
  user_id uuid
);
-- todo comment

create function sg_public.log_in(
  name text,
  password text
) returns sg_public.jwt_token as $$
declare
  user sg_private.user
begin
  select u.* into user
    from sg_private.user as u
    where u.name = $1 or u.email = $1
    limit 1;
  if user.password = crypt(password, user.password) then
    return ('sg_user', user.user_id)::sg_public.jwt_token;
  else
    return null;
  end if;
end;
$$ language plpgsql strict security definer;
comment on function sg_public.log_in(text, text) is 'Logs in a single user.';
-- todo !!! jwt refresh tokens?

------ Users > Permissions (TODO) ----------------------------------------------

------ Users > Triggers (TODO) -------------------------------------------------

create trigger update_user_modified
  before update on sg_public.user
  for each row execute procedure sg_private.update_modified_column();
-- TODO comment

-- TODO Trigger: Create user -> send sign up email

-- TODO Trigger: Update password -> notify user email

------ Users > Capabilities (TODO) ---------------------------------------------

-- Session management
create function sg_public.get_current_user()
returns sg_public.user as $$
  select *
  from sg_public.user
  where id = current_setting('jwt.claims.user_id')::uuid
$$ language sql stable;
comment on function sg_public.get_current_user() is 'Get the current logged in user.';

-- TODO Sign out

-- TODO Get user gravatar

-- TODO Passwords encrypted in DB

-- TODO Send email token / validate token




------ Cards, Units, Subjects --------------------------------------------------

------ Cards, Units, Subjects > Types

create type sg_public.entity_kind as enum(
  'card',
  'unit',
  'subject'
);
-- TODO comment

create type sg_public.entity_status as enum(
  'pending',
  'blocked',
  'declined',
  'accepted'
);
-- TODO comment

create type sg_public.card_kind as enum(
  'video',
  'page',
  'unscored_embed',
  'choice'
);
-- TODO comment

------ Cards, Units, Subjects > Tables

create table sg_public.entity (
  entity_id uuid primary key default uuid_generate_v4(),
  entity_kind sg_public.entity_kind not null
);
-- TODO comment table/columns

create table sg_public.unit_version (
  version_id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  entity_id uuid not null references sg_public.entity (entity_id),  -- TODO enforce kind
  previous_id uuid null references sg_public.unit_version (version_id),
  language varchar(5) not null default 'en'
    constraint lang_check check (language ~* '^\w{2}(-\w{2})?$'),
  name text not null,
  status sg_public.entity_status not null default 'pending',
  available boolean not null default true,
  tags text[] null default array[]::text[],
  user_id uuid not null references sg_public.user (id),  -- TODO allow anonymous
  /* and the rest.... */
  body text not null,
  require_ids uuid[] not null default array[]::uuid[] /* issue no element TODO break into join table */
);

-- TODO comment table/columns/constraints

create table sg_public.subject_version (
  version_id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  entity_id uuid not null references sg_public.entity (entity_id), -- TODO enforce kind
  previous_id uuid null references sg_public.subject_version (version_id),
  language varchar(5)    not null default 'en'
    constraint lang_check check (language ~* '^\w{2}(-\w{2})?$'),
  name text not null,
  status sg_public.entity_status not null default 'pending',
  available boolean not null default true,
  tags text[] null default array[]::text[],
  user_id uuid not null references sg_public.user (id),  -- TODO allow anonymous
  /* and the rest.... */
  body text not null,
  members jsonb not null /* jsonb?: issue cant ref, cant enum composite TODO split into join table */
);

-- TODO comment table/columns/constraints

create table sg_public.card_version (
  version_id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  entity_id uuid not null references sg_public.entity (entity_id), -- TODO enforce kind
  previous_id uuid null references sg_public.card_version (version_id),
  language varchar(5) not null default 'en'
    constraint lang_check check (language ~* '^\w{2}(-\w{2})?$'),
  name text not null,
  status sg_public.entity_status not null default 'pending',
  available boolean not null default true,
  tags text[] null default array[]::text[],
  user_id uuid not null references sg_public.user (id),  -- TODO allow anonymous
  /* and the rest.... */
  unit_id uuid not null references sg_public.entity (entity_id),  -- TODO check kind
  require_ids uuid[] not null default array[]::uuid[], /* issue no element  TODO split into join table */
  kind sg_public.card_kind not null,
  data jsonb not null /* jsonb?: varies per kind */
);

-- TODO create entity `view`s
-- TODO comment table/columns/constraints

create table sg_public.card_parameters (
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  entity_id uuid not null unique references sg_public.entity (entity_id),  -- TODO check kind
  guess_distribution jsonb not null,
    /* jsonb?: map */
  slip_distribution jsonb not null );
-- TODO comment table/columns

------ Cards, Units, Subjects > Validations (TODO)

-- TODO Validation: `data` field of cards by type with JSON schema

-- TODO Validation: No require cycles for units

-- TODO Validation: No require cycles for cards

-- TODO  Validation: No cycles in subject members

-- TODO TODO Who can update entity statuses? How?

------ Cards, Units, Subjects > Sessions (TODO)

------ Cards, Units, Subjects > Permissions (TODO)

-- TODO only the status can change... when

------ Cards, Units, Subjects > Triggers

create trigger update_unit_modified
  before update on sg_public.unit_version
  for each row execute procedure sg_private.update_modified_column(); -- TODO comment

create trigger update_subject_modified
  before update on sg_public.subject_version
  for each row execute procedure sg_private.update_modified_column();  -- TODO comment

create trigger update_card_modified
  before update on sg_public.card_version
  for each row execute procedure sg_private.update_modified_column();  -- TODO comment

create trigger update_card_parameters_modified
  before update on sg_public.card_parameters
  for each row execute procedure sg_private.update_modified_column();  -- TODO comment

------ Cards, Units, Subjects > Capabilities (TODO)

-- TODO Search per entity type

-- TODO Search across entity types

-- TODO List all units of a subject, recursively

-- TODO List all subjects unit belongs to, recursively

-- TODO Get recommended subjects

-- TODO Capability: get entites I've created



------ Topics, Posts, Notices, Follows -----------------------------------------

------ Topics, Posts, Notices, Follows > Types

create type sg_public.post_kind as enum(
  'post',
  'proposal',
  'vote'
);
-- todo comment

create type sg_public.notice_kind as enum(
  'create_topic',
  'create_proposal',
  'block_proposal',
  'decline_proposal',
  'accept_proposal',
  'create_post',
  'come_back'
);
-- todo comment

------ Topics, Posts, Notices, Follows > Tables

create table sg_public.topic (
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  user_id uuid not null references sg_public.user (id),  -- TODO allow anonymous
  name text not null,
  entity_id uuid not null,  /* TODO issue cant ref across tables */
  entity_kind sg_public.entity_kind not null );
-- todo comment table/columns

create table sg_public.post (
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  user_id uuid not null references sg_public.user (id),  -- TODO allow anonymous
  topic_id uuid not null references sg_public.topic (id),
  kind sg_public.post_kind not null default 'post',
  body text null
    check (kind = 'vote' or body is not null),
  replies_to_id uuid null references sg_public.post (id)
    check (kind <> 'vote' or replies_to_id is not null),
  entity_versions jsonb null
    check (kind <> 'proposal' or entity_versions is not null),
    /* jsonb?: issue cant ref, cant enum composite TODO split into join table */
  response boolean null
    check (kind <> 'vote' or response is not null)
);
-- todo comment table/columns

create table sg_public.notice (
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  user_id uuid not null references sg_public.user (id),
  kind sg_public.notice_kind not null,
  data jsonb not null,
    /* jsonb?: varies per kind */
  read boolean not null default false,
  tags text[] null default array[]::text[]
);
-- todo comment table/columns

create table sg_public.follow (
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  user_id uuid not null references sg_public.user (id),
  entity_id uuid not null, /* issue cant ref across tables  TODO fix */
  entity_kind sg_public.entity_kind not null,
  unique (user_id, entity_id)
);
-- todo comment table/columns

------ Topics, Posts, Notices, Follows > Validations todo

-- Post validation: A user can only vote once on a given proposal.
create unique index post_vote_unique_idx
  on sg_public.post (user_id, replies_to_id)
  where kind = 'vote';
-- todo comment

-- TODO Post validation: A reply must belong to the same topic.

-- TODO Post validation: A post can reply to a post, proposal, or vote.

-- TODO Post validation: A proposal can reply to a post, proposal, or vote.

-- TODO Post validation: A vote may only reply to a proposal.

-- TODO Post validation: A vote cannot reply to a proposal that is accepted or declined.

-- TODO Post validation: A user cannot vote on their own proposal.

-- TODO Post validation: For proposals, the status can only be changed to declined, and only when the current status is pending or blocked.

------ Topics, Posts, Notices, Follows > Sessions (todo)

------ Topics, Posts, Notices, Follows > Permissions (todo)

-- TODO Topic permission: Only the author of a topic can edit the name.

-- TODO Post permission: A user can only update: Post: body; Proposal: body; Vote: body, response

-- TODO Permission: a user can only read their own notices and follows

-- TODO Permission: a user can only read/unread their own notices

------ Topics, Posts, Notices, Follows > Triggers (todo)

create trigger update_topic_modified
  before update on sg_public.topic
  for each row execute procedure sg_private.update_modified_column(); -- todo comment

create trigger update_post_modified
  before update on sg_public.post
  for each row execute procedure sg_private.update_modified_column(); -- todo comment

create trigger update_notice_modified
  before update on sg_public.notice
  for each row execute procedure sg_private.update_modified_column(); -- todo comment

create trigger update_follow_modified
  before update on sg_public.follow
  for each row execute procedure sg_private.update_modified_column(); -- todo comment

-- TODO Trigger: when I create or update a vote post, we can update entity status

-- TODO Trigger: create notices when an entity status updates

-- TODO Trigger: create notices when a topic gets a new post

-- TODO Trigger: when I create a topic, I follow the entity

-- TODO Trigger: when I create a post, I follow the entity

------ Topics, Posts, Notices, Follows > Capabilities (todo)

-- Notices > TODO Create notices for all users that follow an entity




------ User Subjects, Responses ------------------------------------------------

------ User Subjects, Responses > Types (TODO)

------ User Subjects, Responses > Tables

create table sg_public.user_subject (
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  user_id uuid not null references sg_public.user (id),
  subject_id uuid not null references sg_public.entity (entity_id), --  TODO check kind
  unique (user_id, subject_id)
);
-- todo comment table/columns

create table sg_public.response (
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  user_id uuid not null references sg_public.user (id),  -- TODO allow anonymous
  card_id uuid not null references sg_public.entity (entity_id),  -- TODO check kind
  unit_id uuid not null references sg_public.entity (entity_id),  -- TODO check kind
  response text not null,
  score double precision not null check (score >= 0 and score <= 1),
  learned double precision not null check (score >= 0 and score <= 1)
);
-- todo comment table/columns

------ User Subjects, Responses > Validations (todo)

------ User Subjects, Responses > Sessions (todo)

------ User Subjects, Responses > Permissions (todo)

-- TODO  Permission: A user can only create/read/update their own usubjs

------ User Subjects, Responses > Triggers

create trigger update_user_subject_modified
  before update on sg_public.user_subject
  for each row execute procedure sg_private.update_modified_column();
-- todo comment

create trigger update_response_modified
  before update on sg_public.response
  for each row execute procedure sg_private.update_modified_column();
-- todo comment

/* TODO
- Trigger: Create response ->
  - Update p(learned)
  - Calculate updated guess value
  - Calculate updated slip value
  - Calculate updated transit value
*/

------ User Subjects, Responses > Capabilities (todo)

-- TODO Get and set learning context

-- TODO Get latest response user x unit

-- TODO? Calculate the mean value of a PMF

-- TODO Calculated learned x belief

-- TODO Validate & score card response

-- TODO After I select a subject, traverse the units to give the learner some units to pick

-- TODO After I select a unit, or respond to a card, search for a suitable card

-- TODO Respond to a card

-- TODO When p(L) > 0.99, return to choose a unit



------ Suggests, Suggest Followers ---------------------------------------------

------ Suggests, Suggest Followers > Types - N/A

------ Suggests, Suggest Followers > Tables

create table sg_public.suggest (
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  name text not null,
  body text null );
-- todo comment table/columns

create table sg_public.suggest_follower (
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  suggest_id uuid not null references sg_public.suggest (id),
  email text null, -- todo this must be private, or delete it?
  user_id uuid null references sg_public.user (id),
  unique (suggest_id, user_id)
);
-- todo comment table/columns

------ Suggests, Suggest Followers > Validations (todo)

------ Suggests, Suggest Followers > Sessions (todo)

------ Suggests, Suggest Followers > Permissions (todo)

------ Suggests, Suggest Followers > Triggers (todo)

create trigger update_suggest_modified
  before update on sg_public.suggest
  for each row execute procedure sg_private.update_modified_column();
-- todo comment

create trigger update_suggest_follower_modified
  before update on sg_public.suggest_follower
  for each row execute procedure sg_private.update_modified_column();
-- todo comment

------ Suggests, Suggest Followers > Capabilities (todo)
