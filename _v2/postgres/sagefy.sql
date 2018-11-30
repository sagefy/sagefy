-- This file should be kept up-to-date as the latest, current version.
-- We can use this file for local development, testing, reference, debugging, and evaluation.


-- ENSURE UTF-8

create extension if not exists "uuid-ossp";
create extension if not exists "pgcrypto";




------ Generic -----------------------------------------------------------------

------ Generic > Schemas and Roles ---------------------------------------------

create schema sg_public; -- Exposed to GraphQL
create schema sg_hidden; -- Not exposed to GraphQL
create schema sg_private; -- Secrets
-- todo comment

create role sg_postgraphile login password 'xyz'; -- todo !!! fix password
create role sg_admin;
create role sg_user;
create role sg_anonymous;
grant sg_admin to sg_postgraphile;
grant sg_user to sg_postgraphile;
grant sg_anonymous to sg_postgraphile;
-- todo comment on roles

-- Disable function execution permission by default.
alter default privileges revoke execute on functions from public;

-- Allow everyone to see the sg_public schema exists.
grant usage on schema sg_public to sg_anonymous, sg_user, sg_admin;

------ Generic > Trigger Functions ---------------------------------------------

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
-- todo comment

create type sg_public.jwt_token as (
  role text,
  user_id uuid
);
-- todo comment

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

------ Users > Sessions --------------------------------------------------------

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
    return ('sg_user', user.user_id)::sg_public.jwt_token; -- todo handle if admin
  else
    return null;
  end if;
end;
$$ language plpgsql strict security definer;
comment on function sg_public.log_in(text, text) is 'Logs in a single user.';
-- todo !!! jwt refresh tokens?

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

-- TODO Send email token / validate token / update email

------ Users > Permissions -----------------------------------------------------

-- No one other than Postgraphile has access to sg_private.

-- Enable RLS.
alter table sg_public.user enable row level security;

-- Select user: any.
grant select on table sg_public.user to sg_anonymous, sg_user, sg_admin;
create policy select_user on sg_public.user
  for select -- any user
  using (true); -- TODO comment

-- Insert user: only anonymous, via function.
grant execute on function sg_public.sign_up(text, text, text) to sg_anonymous;

-- Update user: user self (name, settings), or admin.
grant update on table sg_public.user to sg_user, sg_admin;
create policy update_user on sg_public.user
  for update (name, view_subjects) to sg_user
  using (id = current_setting('jwt.claims.user_id')::uuid); -- TODO comment
create policy update_user_admin on sg_public.user
  for update to sg_admin
  using (true); -- TODO comment

-- Delete user: user self, or admin.
grant delete on table sg_public.user to sg_user, sg_admin;
create policy delete_user on sg_public.user
  for delete to sg_user
  using (id = current_setting('jwt.claims.user_id')::uuid); -- TODO comment
create policy delete_user_admin on sg_public.user
  for delete to sg_admin
  using (true); -- TODO comment

-- All users may log in or check the current user.
grant execute on function sg_public.log_in(text, text) to sg_anonymous, sg_user, sg_admin;
grant execute on function sg_public.get_current_user() to sg_anonymous, sg_user, sg_admin;
-- todo other functions...








------ Cards, Units, Subjects --------------------------------------------------

------ Cards, Units, Subjects > Types ------------------------------------------

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

------ Cards, Units, Subjects > Tables -----------------------------------------

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
  -- and the rest....
  body text not null,
  require_ids uuid[] not null default array[]::uuid[] -- issue no element TODO break into join table
);
-- TODO comment table/columns/constraints

create view sg_public.unit as
  select distinct on (entity_id) *
  from sg_public.unit_version
  where status = 'accepted'
  order by entity_id, created desc;
-- todo comment

create table sg_public.subject_version (
  version_id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  entity_id uuid not null references sg_public.entity (entity_id), -- TODO enforce kind
  previous_id uuid null references sg_public.subject_version (version_id),
  language varchar(5) not null default 'en'
    constraint lang_check check (language ~* '^\w{2}(-\w{2})?$'),
  name text not null,
  status sg_public.entity_status not null default 'pending',
  available boolean not null default true,
  tags text[] null default array[]::text[],
  user_id uuid not null references sg_public.user (id),  -- TODO allow anonymous
  -- and the rest....
  body text not null,
  members jsonb not null -- jsonb?: issue cant ref, cant enum composite TODO split into join table
);
-- TODO comment table/columns/constraints

create view sg_public.subject as
  select distinct on (entity_id) *
  from sg_public.subject_version
  where status = 'accepted'
  order by entity_id, created desc;
-- todo comment

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
  -- and the rest....
  unit_id uuid not null references sg_public.entity (entity_id),  -- TODO check kind
  require_ids uuid[] not null default array[]::uuid[], -- issue no element  TODO split into join table
  kind sg_public.card_kind not null,
  data jsonb not null -- jsonb?: varies per kind
);
-- TODO create entity `view`s
-- TODO comment table/columns/constraints

create table sg_public.card_parameters (
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  entity_id uuid not null unique references sg_public.entity (entity_id),  -- TODO check kind
  guess_distribution jsonb not null,
    -- jsonb?: map
  slip_distribution jsonb not null );
-- TODO comment table/columns

create view sg_public.card as
  select distinct on (entity_id) *
  from sg_public.card_version
  where status = 'accepted'
  order by entity_id, created desc;
-- todo comment
-- todo join with parameters in view?

------ Cards, Units, Subjects > Validations (TODO) -----------------------------

-- TODO Validation: `data` field of cards by type with JSON schema

-- TODO Validation: No require cycles for units

-- TODO Validation: No require cycles for cards

-- TODO  Validation: No cycles in subject members

-- TODO TODO Who can update entity statuses? How?

------ Cards, Units, Subjects > Triggers ---------------------------------------

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

------ Cards, Units, Subjects > Capabilities (TODO) ----------------------------

-- TODO Search per entity type

-- TODO Search across entity types

-- TODO List all units of a subject, recursively

-- TODO List all subjects unit belongs to, recursively

-- TODO Get recommended subjects

-- TODO Capability: get entites I've created

-- TODO insert new / new version of existing

------ Cards, Units, Subjects > Permissions ------------------------------------


-- Select card, unit, subject: any.
grant select on table sg_public.unit_version to sg_anonymous, sg_user, sg_admin;
grant select on table sg_public.subject_version to sg_anonymous, sg_user, sg_admin;
grant select on table sg_public.card_version to sg_anonymous, sg_user, sg_admin;
grant select on table sg_public.card_parameters to sg_anonymous, sg_user, sg_admin;

-- Insert (or new version) card, unit, subject: any via function.
grant execute on function sg_public.new_unit(???) to sg_anonymous, sg_user, sg_admin;
grant execute on function sg_public.edit_unit(???) to sg_anonymous, sg_user, sg_admin;
grant execute on function sg_public.new_subject(???) to sg_anonymous, sg_user, sg_admin;
grant execute on function sg_public.edit_subject(???) to sg_anonymous, sg_user, sg_admin;
grant execute on function sg_public.new_card(???) to sg_anonymous, sg_user, sg_admin;
grant execute on function sg_public.edit_card(???) to sg_anonymous, sg_user, sg_admin;

-- Update & delete card, unit, subject: admin.
grant update, delete on table sg_public.unit_version to sg_admin;
grant update, delete on table sg_public.subject_version to sg_admin;
grant update, delete on table sg_public.card_version to sg_admin;
grant update, delete on table sg_public.card_parameters to sg_admin;

-- todo other functions...







------ Topics, Posts, Notices, Follows -----------------------------------------

------ Topics, Posts, Notices, Follows > Types ---------------------------------

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

------ Topics, Posts, Notices, Follows > Tables --------------------------------

create table sg_public.topic (
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  user_id uuid not null references sg_public.user (id),  -- TODO allow anonymous
  name text not null,
  entity_id uuid not null, -- TODO issue cant ref across tables
  -- todo verify id x kind
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
    -- jsonb?: issue cant ref, cant enum composite TODO split into join table
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
    -- jsonb?: varies per kind
  read boolean not null default false,
  tags text[] null default array[]::text[]
);
-- todo comment table/columns

create table sg_public.follow (
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  user_id uuid not null references sg_public.user (id),
  entity_id uuid not null, -- issue cant ref across tables  TODO fix
  entity_kind sg_public.entity_kind not null,
  unique (user_id, entity_id)
);
-- todo comment table/columns

------ Topics, Posts, Notices, Follows > Validations todo ----------------------

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

------ Topics, Posts, Notices, Follows > Triggers (todo) -----------------------

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

------ Topics, Posts, Notices, Follows > Capabilities (todo) -------------------

-- Notices > TODO Create notices for all users that follow an entity

------ Topics, Posts, Notices, Follows > Permissions ---------------------------

-- Enable RLS.
alter table sg_public.topic enable row level security;
alter table sg_public.post enable row level security;
alter table sg_public.notice enable row level security;
alter table sg_public.follow enable row level security;

-- Select topic: any.
grant select on table sg_public.topic to sg_anonymous, sg_user, sg_admin;
create policy select_topic on sg_public.topic
  for select -- any user
  using (true); -- TODO comment

-- Insert topic: any via function.
-- todo

-- Update topic: user self (name), or admin.
grant update on table sg_public.topic to sg_user, sg_admin;
create policy update_topic on sg_public.topic
  for update (name) to sg_user
  using (user_id = current_setting('jwt.claims.user_id')::uuid); -- TODO comment
create policy update_topic_admin on sg_public.topic
  for update to sg_admin
  using (true); -- TODO comment

-- Delete topic: admin.
grant delete on table sg_public.topic to sg_admin;
create policy delete_topic_admin on sg_public.topic
  for delete to sg_admin
  using (true); -- TODO comment

-- Select post: any.
grant select on table sg_public.post to sg_anonymous, sg_user, sg_admin;
create policy select_post on sg_public.post
  for select -- any user
  using (true); -- TODO comment

-- Insert post: any via function.
-- todo

-- Update post: user self (body, response), or admin.
grant update on table sg_public.post to sg_user, sg_admin;
create policy update_post on sg_public.post
  for update (body, response) to sg_user
  using (user_id = current_setting('jwt.claims.user_id')::uuid); -- TODO comment
create policy update_post_admin on sg_public.post
  for update to sg_admin
  using (true); -- TODO comment

-- Delete post: admin.
grant delete on table sg_public.post to sg_admin;
create policy delete_post_admin on sg_public.post
  for delete to sg_admin
  using (true); -- TODO comment

-- Select follow: user or admin self.
grant select on table sg_public.follow to sg_user, sg_admin;
create policy select_follow on sg_public.follow
  for select to sg_user, sg_admin
  using (user_id = current_setting('jwt.claims.user_id')::uuid); -- TODO comment

-- Insert follow: user or admin via function.
-- TODO or does this need to be a function?

-- Update follow: none.

-- Delete follow: user or admin self.
grant delete on table sg_public.follow to sg_user, sg_admin;
create policy delete_follow on sg_public.follow
  for select to sg_user, sg_admin
  using (user_id = current_setting('jwt.claims.user_id')::uuid); -- TODO comment

-- Select notice: user or admin self.
grant select on table sg_public.notice to sg_user, sg_admin;
create policy select_notice on sg_public.notice
  for select to sg_user, sg_admin
  using (user_id = current_setting('jwt.claims.user_id')::uuid); -- TODO comment

-- Insert notice: none.

-- Update notice: user or admin self (read).
grant update on table sg_public.notice to sg_user, sg_admin;
create policy update_notice on sg_public.notice
  for update (read) to sg_user, sg_admin
  using (user_id = current_setting('jwt.claims.user_id')::uuid); -- TODO comment

-- Delete notice: user or admin self.
grant delete on table sg_public.notice to sg_user, sg_admin;
create policy delete_notice on sg_public.notice
  for delete to sg_user, sg_admin
  using (user_id = current_setting('jwt.claims.user_id')::uuid); -- TODO comment

-- todo function permissions...














------ User Subjects, Responses ------------------------------------------------

------ User Subjects, Responses > Types (TODO) ---------------------------------

------ User Subjects, Responses > Tables ---------------------------------------

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

------ User Subjects, Responses > Validations (todo) ---------------------------

------ User Subjects, Responses > Triggers -------------------------------------

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

------ User Subjects, Responses > Capabilities (todo) --------------------------

-- TODO Get and set learning context

-- TODO Get latest response user x unit

-- TODO? Calculate the mean value of a PMF

-- TODO Calculated learned x belief

-- TODO Validate & score card response

-- TODO After I select a subject, traverse the units to give the learner some units to pick

-- TODO After I select a unit, or respond to a card, search for a suitable card

-- TODO Respond to a card

-- TODO When p(L) > 0.99, return to choose a unit

------ User Subjects, Responses > Permissions ----------------------------------

-- Enable RLS.
alter table sg_public.user_subject enable row level security;
alter table sg_public.response enable row level security;

-- Select usubj: user or admin self or with setting.
-- TODO

-- Insert usubj: user or admin via function.
-- TODO or does it need to be a function?

-- Update usubj: none.

-- Delete usubj: user or admin self.
grant delete on table sg_public.user_subject to sg_user, sg_admin;
create policy delete_user_subject on sg_public.user_subject
  for delete to sg_user, sg_admin
  using (id = current_setting('jwt.claims.user_id')::uuid); -- TODO comment

-- Select response: any self.
-- TODO

-- Insert response: any via function.
-- TODO

-- Update & delete response: none.

-- TODO other functions...










------ Suggests, Suggest Followers ---------------------------------------------

------ Suggests, Suggest Followers > Types - N/A -------------------------------

------ Suggests, Suggest Followers > Tables ------------------------------------

create table sg_public.suggest (
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  name text not null,
  body text null
);
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

------ Suggests, Suggest Followers > Validations (todo) ------------------------

------ Suggests, Suggest Followers > Triggers (todo) ---------------------------

create trigger update_suggest_modified
  before update on sg_public.suggest
  for each row execute procedure sg_private.update_modified_column();
-- todo comment

create trigger update_suggest_follower_modified
  before update on sg_public.suggest_follower
  for each row execute procedure sg_private.update_modified_column();
-- todo comment

------ Suggests, Suggest Followers > Capabilities (todo) -----------------------

------ Suggests, Suggest Followers > Permissions -------------------------------

-- Enable RLS.
alter table sg_public.suggest_follower enable row level security;

-- Select suggest: any.
grant select on table sg_public.suggest to sg_anonymous, sg_user, sg_admin;

-- Insert suggest: any via function.
-- TODO

-- Update suggest: admin.
grant update on table sg_public.suggest to sg_admin;

-- Delete suggest: admin.
grant delete on table sg_public.suggest to sg_admin;

-- Select suggest_follower: any.
grant select on table sg_public.suggest_follower to sg_anonymous, sg_user, sg_admin;
create policy select_suggest_follower on sg_public.suggest_follower
  for select -- any user
  using (true); -- TODO comment

-- Insert suggest_follower: any via function above.

-- Update suggest_follow: none.

-- Delete suggest_follow: user or admin self.
grant delete on table sg_public.suggest_follower to sg_user, sg_admin;
create policy delete_suggest_follower on sg_public.suggest_follower
  for delete to sg_user, sg_admin
  using (id = current_setting('jwt.claims.user_id')::uuid); -- TODO comment

-- TODO other functions...
