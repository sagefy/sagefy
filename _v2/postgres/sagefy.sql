# This file should be kept up-to-date as the latest, current version.

# ENSURE UTF-8

create extension if not exists "uuid-ossp";
create extension if not exists "pgcrypto";


## Generic > Trigger Functions

create or replace function update_modified_column()
returns trigger as $$
begin new.modified = now();
  return new;
end;
$$ language 'plpgsql';




### Users ######################################################################

### Users > Types -- N/A

### Users > Tables

create table user (  # todo schema
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  name text not null unique,
  email text not null unique constraint email_check check (email ~* '^\s+@\s+\.\s+$'), # todo move to private table
  password varchar(60) not null constraint pass_check check (password ~* '^\$2\w\$.*$'), # todo move to private table
  settings jsonb not null /* jsonb?: add new settings without alter table */ # todo move to private table
);

### Users > Validations

### Users > Sessions

### Users > Permissions

### Users > Triggers

create trigger update_user_modified before update on user for each row execute procedure update_modified_column(); # TODO schema?

# TODO Trigger: Create user -> send sign up email

# TODO Trigger: Update password -> notify user email

### Users > Capabilities

# TODO Session management (log in/logged in/sign out)

# TODO Get user gravatar

# TODO Passwords encrypted in DB

# TODO Send email token / validate token




### Cards, Units, Subjects #####################################################

### Cards, Units, Subjects > Types

create type entity_kind as enum( # todo schema
  'card',
  'unit',
  'subject'
);

create type entity_status as enum( # todo schema
  'pending',
  'blocked',
  'declined',
  'accepted'
);

create type card_kind as enum( # todo schema
  'video',
  'page',
  'unscored_embed',
  'choice'
);

### Cards, Units, Subjects > Tables

create table entity (
  entity_id uuid primary key default uuid_generate_v4(),
  entity_kind entity_kind not null
)

create table unit_version ( # TODO schema
  version_id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  entity_id uuid not null references entity (entity_id),  # TODO enforce kind
  previous_id uuid null references unit_version (version_id),
  language varchar(5) not null default 'en'
    constraint lang_check check (language ~* '^\w{2}(-\w{2})?$'),
  name text not null,
  status entity_status not null default 'pending',
  available boolean not null default true,
  tags text[] null default array[]::text[],
  user_id uuid not null references user (id),  # TODO allow anonymous
  /* and the rest.... */
  body text not null,
  require_ids uuid[] not null default array[]::uuid[] /* issue no element TODO break into join table */
);

create table subject_version ( # TODO schema
  version_id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  entity_id uuid not null references entity (entity_id), # TODO enforce kind
  previous_id uuid null references subject_version (version_id),
  language varchar(5)    not null default 'en'
    constraint lang_check check (language ~* '^\w{2}(-\w{2})?$'),
  name text not null,
  status entity_status not null default 'pending',
  available boolean not null default true,
  tags text[] null default array[]::text[],
  user_id uuid not null references user (id),  # TODO allow anonymous
  /* and the rest.... */
  body text not null,
  members jsonb not null /* jsonb?: issue cant ref, cant enum composite TODO split into join table */
);

create table card_version ( # TODO schema
  version_id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  entity_id uuid not null references entity (entity_id), # TODO enforce kind
  previous_id uuid null references card_version (version_id),
  language varchar(5) not null default 'en'
    constraint lang_check check (language ~* '^\w{2}(-\w{2})?$'),
  name text not null,
  status entity_status not null default 'pending',
  available boolean not null default true,
  tags text[] null default array[]::text[],
  user_id uuid not null references user (id),  # TODO allow anonymous
  /* and the rest.... */
  unit_id uuid not null references entity (entity_id),  # TODO check kind
  require_ids uuid[] not null default array[]::uuid[], /* issue no element  TODO split into join table */
  kind card_kind not null,
  data jsonb not null /* jsonb?: varies per kind */
);

# TODO create entity `view`s

create table card_parameters ( # TODO schema
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  entity_id uuid not null unique references entity (entity_id),  # TODO check kind
  guess_distribution jsonb not null,
    /* jsonb?: map */
  slip_distribution jsonb not null );

### Cards, Units, Subjects > Validations

# TODO Validation: `data` field of cards by type

# TODO Validation: No require cycles for units

# TODO Validation: No require cycles for cards

# TODO  Validation: No cycles in subject members

# TODO TODO Who can update entity statuses? How?

### Cards, Units, Subjects > Sessions

### Cards, Units, Subjects > Permissions

### Cards, Units, Subjects > Triggers

create trigger update_unit_modified before update on unit for each row execute procedure update_modified_column(); # TODO schema? 

create trigger update_subject_modified before update on subject for each row execute procedure update_modified_column(); # TODO schema?

create trigger update_card_modified before update on card for each row execute procedure update_modified_column(); # TODO schema?

create trigger update_card_parameters_modified before update on card_parameters for each row execute procedure update_modified_column(); # TODO schema?

### Cards, Units, Subjects > Capabilities

# TODO Search per entity type

# TODO Search across entity types

# TODO List all units of a subject, recursively

# TODO List all subjects unit belongs to, recursively

# TODO Get recommended subjects

# TODO Capability: get entites I've created



### Topics, Posts, Notices, Follows ############################################

### Topics, Posts, Notices, Follows > Types

create type post_kind as enum( # todo schema
  'post',
  'proposal',
  'vote'
);

create type notice_kind as enum( # todo schema
  'create_topic',
  'create_proposal',
  'block_proposal',
  'decline_proposal',
  'accept_proposal',
  'create_post',
  'come_back'
);

### Topics, Posts, Notices, Follows > Tables

create table topic ( # TODO schema
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  user_id uuid not null references user (id),  # TODO allow anonymous
  name text not null,
  entity_id uuid not null,  /* TODO issue cant ref across tables */
  entity_kind entity_kind not null );

create table post ( # TODO schema
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  user_id uuid not null references user (id),  # TODO allow anonymous
  topic_id uuid not null references topic (id),  
  kind post_kind not null default 'post',
  body text null check (kind = 'vote' or body is not null),
  replies_to_id uuid null references post (id)
    check (kind <> 'vote' or replies_to_id is not null),
  entity_versions jsonb null check (kind <> 'proposal' or entity_versions is not null),
    /* jsonb?: issue cant ref, cant enum composite TODO split into join table */
  response boolean null check (kind <> 'vote' or response is not null)
);

create table notice ( # TODO schema
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  user_id uuid not null references user (id),
  kind notice_kind not null,
  data jsonb not null,
    /* jsonb?: varies per kind */
  read boolean not null default false,
  tags text[] null default array[]::text[]
);

create table follow (  # TODO schema
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  user_id uuid not null references user (id),
  entity_id uuid not null, /* issue cant ref across tables  TODO fix */
  entity_kind entity_kind not null,
  unique (user_id, entity_id)
);

### Topics, Posts, Notices, Follows > Validations

# Post validation: A user can only vote once on a given proposal.
create unique index posts_vote_unique_idx on posts (user_id, replies_to_id) where kind = 'vote';

# TODO Post validation: A reply must belong to the same topic.

# TODO Post validation: A post can reply to a post, proposal, or vote.

# TODO Post validation: A proposal can reply to a post, proposal, or vote.

# TODO Post validation: A vote may only reply to a proposal.

# TODO Post validation: A vote cannot reply to a proposal that is accepted or declined.

# TODO Post validation: A user cannot vote on their own proposal.

# TODO Post validation: For proposals, the status can only be changed to declined, and only when the current status is pending or blocked.

### Topics, Posts, Notices, Follows > Sessions

### Topics, Posts, Notices, Follows > Permissions

# TODO Topic permission: Only the author of a topic can edit the name.

# TODO Post permission: A user can only update: Post: body; Proposal: body; Vote: body, response

# TODO Permission: a user can only read their own notices and follows

# TODO Permission: a user can only read/unread their own notices

### Topics, Posts, Notices, Follows > Triggers

create trigger update_topic_modified before update on topic for each row execute procedure update_modified_column(); # TODO schema?

create trigger update_post_modified before update on post for each row execute procedure update_modified_column(); # TODO schema?

create trigger update_notice_modified before update on notice for each row execute procedure update_modified_column(); # TODO schema?

create trigger update_follow_modified before update on follow for each row execute procedure update_modified_column(); # TODO schema?

# TODO Trigger: when I create or update a vote post, we can update entity status

# TODO Trigger: create notices when an entity status updates

# TODO Trigger: create notices when a topic gets a new post

# TODO Trigger: when I create a topic, I follow the entity

# TODO Trigger: when I create a post, I follow the entity

### Topics, Posts, Notices, Follows > Capabilities

# Notices > TODO Create notices for all users that follow an entity




### User Subjects, Responses ###################################################

### User Subjects, Responses > Types

### User Subjects, Responses > Tables

create table user_subject ( # TODO schema
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  user_id uuid not null references user (id),
  subject_id uuid not null references entity (entity_id), #  TODO check kind
  unique (user_id, subject_id)
);

create table response ( # TODO schema
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  user_id uuid not null references user (id),  # TODO allow anonymous
  card_id uuid not null references entity (entity_id),  # TODO check kind
  unit_id uuid not null references entity (entity_id),  # TODO check kind
  response text not null,
  score double precision not null check (score >= 0 and score <= 1),
  learned double precision not null check (score >= 0 and score <= 1)
);

### User Subjects, Responses > Validations

### User Subjects, Responses > Sessions

### User Subjects, Responses > Permissions

# TODO  Permission: A user can only create/read/update their own usubjs

### User Subjects, Responses > Triggers

create trigger update_user_subject_modified before update on user_subject for each row execute procedure update_modified_column(); # TODO schema?

create trigger update_response_modified before update on response for each row execute procedure update_modified_column(); # TODO schema?

/* TODO 
- Trigger: Create response ->
  - Update p(learned)
  - Calculate updated guess value
  - Calculate updated slip value
  - Calculate updated transit value
*/

### User Subjects, Responses > Capabilities

# TODO Get and set learning context

# TODO Get latest response user x unit

# TODO? Calculate the mean value of a PMF

# TODO Calculated learned x belief

# TODO Validate & score card response

# TODO After I select a subject, traverse the units to give the learner some units to pick

# TODO After I select a unit, or respond to a card, search for a suitable card

# TODO Respond to a card

# TODO When p(L) > 0.99, return to choose a unit



### Suggests, Suggest Followers ################################################

### Suggests, Suggest Followers > Types

### Suggests, Suggest Followers > Tables


create table suggest ( # TODO schema
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  name text not null,
  body text null ); 

create table suggest_follower ( # TODO schema
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  suggest_id uuid not null references suggest (id),
  email text null,
  session_id uuid null,
  user_id uuid null,  # TODO allow anonymous. add references
  check (session_id is not null or user_id is not null),
  unique (suggest_id, session_id),
  unique (suggest_id, user_id)
);

### Suggests, Suggest Followers > Validations

### Suggests, Suggest Followers > Sessions

### Suggests, Suggest Followers > Permissions

### Suggests, Suggest Followers > Triggers

create trigger update_suggest_modified before update on suggest for each row execute procedure update_modified_column(); # TODO schema?

create trigger update_suggest_follower_modified before update on suggest_follower for each row execute procedure update_modified_column(); # TODO schema?

### Suggests, Suggest Followers > Capabilities
