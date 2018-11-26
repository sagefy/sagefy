-- This file should be kept up-to-date as the latest, current version.

-- ENSURE UTF-8

create extension if not exists "uuid-ossp";
create extension if not exists "pgcrypto";

---- Generic > Schemas

create schema sg_public; -- Exposed to GraphQL
create schema sg_hidden; -- Not exposed to GraphQL
create schema sg_private; -- Secrets


---- Generic > Trigger Functions

create or replace function sg_private.update_modified_column()
returns trigger as $$
begin new.modified = now();
  return new;
end;
$$ language 'plpgsql';


------ Users -------------------------------------------------------------------

------ Users > Types -- N/A

------ Users > Tables

create table sg_public.user (
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  name text not null unique,
  email text not null unique constraint email_check check (email ~* '^\S+@\S+\.\S+$'), -- todo move to private table
  password varchar(60) not null constraint pass_check check (password ~* '^\$2\w\$.*$'), -- todo move to private table
  settings jsonb not null /* jsonb?: add new settings without alter table */ -- todo move to private table
);

------ Users > Validations

------ Users > Sessions

------ Users > Permissions

------ Users > Triggers

create trigger update_user_modified before update on sg_public.user for each row execute procedure sg_private.update_modified_column();

-- TODO Trigger: Create user -> send sign up email

-- TODO Trigger: Update password -> notify user email

------ Users > Capabilities

-- TODO Session management (log in/logged in/sign out)

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

create type sg_public.entity_status as enum(
  'pending',
  'blocked',
  'declined',
  'accepted'
);

create type sg_public.card_kind as enum(
  'video',
  'page',
  'unscored_embed',
  'choice'
);

------ Cards, Units, Subjects > Tables

create table sg_public.entity (
  entity_id uuid primary key default uuid_generate_v4(),
  entity_kind sg_public.entity_kind not null
);

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

create table sg_public.card_parameters (
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  entity_id uuid not null unique references sg_public.entity (entity_id),  -- TODO check kind
  guess_distribution jsonb not null,
    /* jsonb?: map */
  slip_distribution jsonb not null );

------ Cards, Units, Subjects > Validations

-- TODO Validation: `data` field of cards by type with JSON schema

-- TODO Validation: No require cycles for units

-- TODO Validation: No require cycles for cards

-- TODO  Validation: No cycles in subject members

-- TODO TODO Who can update entity statuses? How?

------ Cards, Units, Subjects > Sessions

------ Cards, Units, Subjects > Permissions

-- TODO only the status can change... when

------ Cards, Units, Subjects > Triggers

create trigger update_unit_modified before update on sg_public.unit_version for each row execute procedure sg_private.update_modified_column(); 

create trigger update_subject_modified before update on sg_public.subject_version for each row execute procedure sg_private.update_modified_column(); 

create trigger update_card_modified before update on sg_public.card_version for each row execute procedure sg_private.update_modified_column(); 

create trigger update_card_parameters_modified before update on sg_public.card_parameters for each row execute procedure sg_private.update_modified_column(); 

------ Cards, Units, Subjects > Capabilities

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

create type sg_public.notice_kind as enum(
  'create_topic',
  'create_proposal',
  'block_proposal',
  'decline_proposal',
  'accept_proposal',
  'create_post',
  'come_back'
);

------ Topics, Posts, Notices, Follows > Tables

create table sg_public.topic ( 
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  user_id uuid not null references sg_public.user (id),  -- TODO allow anonymous
  name text not null,
  entity_id uuid not null,  /* TODO issue cant ref across tables */
  entity_kind sg_public.entity_kind not null );

create table sg_public.post (
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  user_id uuid not null references sg_public.user (id),  -- TODO allow anonymous
  topic_id uuid not null references sg_public.topic (id),  
  kind sg_public.post_kind not null default 'post',
  body text null check (kind = 'vote' or body is not null),
  replies_to_id uuid null references sg_public.post (id)
    check (kind <> 'vote' or replies_to_id is not null),
  entity_versions jsonb null check (kind <> 'proposal' or entity_versions is not null),
    /* jsonb?: issue cant ref, cant enum composite TODO split into join table */
  response boolean null check (kind <> 'vote' or response is not null)
);

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

create table sg_public.follow (
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  user_id uuid not null references sg_public.user (id),
  entity_id uuid not null, /* issue cant ref across tables  TODO fix */
  entity_kind sg_public.entity_kind not null,
  unique (user_id, entity_id)
);

------ Topics, Posts, Notices, Follows > Validations

-- Post validation: A user can only vote once on a given proposal.
create unique index post_vote_unique_idx on sg_public.post (user_id, replies_to_id) where kind = 'vote';

-- TODO Post validation: A reply must belong to the same topic.

-- TODO Post validation: A post can reply to a post, proposal, or vote.

-- TODO Post validation: A proposal can reply to a post, proposal, or vote.

-- TODO Post validation: A vote may only reply to a proposal.

-- TODO Post validation: A vote cannot reply to a proposal that is accepted or declined.

-- TODO Post validation: A user cannot vote on their own proposal.

-- TODO Post validation: For proposals, the status can only be changed to declined, and only when the current status is pending or blocked.

------ Topics, Posts, Notices, Follows > Sessions

------ Topics, Posts, Notices, Follows > Permissions

-- TODO Topic permission: Only the author of a topic can edit the name.

-- TODO Post permission: A user can only update: Post: body; Proposal: body; Vote: body, response

-- TODO Permission: a user can only read their own notices and follows

-- TODO Permission: a user can only read/unread their own notices

------ Topics, Posts, Notices, Follows > Triggers

create trigger update_topic_modified before update on sg_public.topic for each row execute procedure sg_private.update_modified_column();

create trigger update_post_modified before update on sg_public.post for each row execute procedure sg_private.update_modified_column();

create trigger update_notice_modified before update on sg_public.notice for each row execute procedure sg_private.update_modified_column();

create trigger update_follow_modified before update on sg_public.follow for each row execute procedure sg_private.update_modified_column();

-- TODO Trigger: when I create or update a vote post, we can update entity status

-- TODO Trigger: create notices when an entity status updates

-- TODO Trigger: create notices when a topic gets a new post

-- TODO Trigger: when I create a topic, I follow the entity

-- TODO Trigger: when I create a post, I follow the entity

------ Topics, Posts, Notices, Follows > Capabilities

-- Notices > TODO Create notices for all users that follow an entity




------ User Subjects, Responses ------------------------------------------------

------ User Subjects, Responses > Types

------ User Subjects, Responses > Tables

create table sg_public.user_subject (
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  user_id uuid not null references sg_public.user (id),
  subject_id uuid not null references sg_public.entity (entity_id), --  TODO check kind
  unique (user_id, subject_id)
);

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

------ User Subjects, Responses > Validations

------ User Subjects, Responses > Sessions

------ User Subjects, Responses > Permissions

-- TODO  Permission: A user can only create/read/update their own usubjs

------ User Subjects, Responses > Triggers

create trigger update_user_subject_modified before update on sg_public.user_subject for each row execute procedure sg_private.update_modified_column();

create trigger update_response_modified before update on sg_public.response for each row execute procedure sg_private.update_modified_column();

/* TODO 
- Trigger: Create response ->
  - Update p(learned)
  - Calculate updated guess value
  - Calculate updated slip value
  - Calculate updated transit value
*/

------ User Subjects, Responses > Capabilities

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

------ Suggests, Suggest Followers > Types

------ Suggests, Suggest Followers > Tables


create table sg_public.suggest (
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  name text not null,
  body text null ); 

create table sg_public.suggest_follower (
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  suggest_id uuid not null references sg_public.suggest (id),
  email text null,
  user_id uuid null references sg_public.user (id),
  unique (suggest_id, user_id)
);

------ Suggests, Suggest Followers > Validations

------ Suggests, Suggest Followers > Sessions

------ Suggests, Suggest Followers > Permissions

------ Suggests, Suggest Followers > Triggers

create trigger update_suggest_modified before update on sg_public.suggest for each row execute procedure sg_private.update_modified_column();

create trigger update_suggest_follower_modified before update on sg_public.suggest_follower for each row execute procedure sg_private.update_modified_column();

------ Suggests, Suggest Followers > Capabilities
