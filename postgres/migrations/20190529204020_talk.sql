-- migrate:up

create type sg_public.post_kind as enum(
  'post',
  'proposal',
  'vote'
);
comment on type sg_public.post_kind
  is 'The three kinds of posts.';

create table sg_public.topic (
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  user_id uuid null references sg_public.user (id),
  session_id uuid null,
  name text not null,
  entity_id uuid not null,
  entity_kind sg_public.entity_kind not null,
  foreign key (entity_id, entity_kind)
    references sg_public.entity (entity_id, entity_kind),
  constraint user_or_session check (((user_id is not null) or (session_id is not null)))
);

comment on table sg_public.topic
  is 'The topics on an entity''s talk page.';
comment on column sg_public.topic.id
  is 'The public ID of the topic.';
comment on column sg_public.topic.created
  is 'When the user created the topic.';
comment on column sg_public.topic.modified
  is 'When the user last modified the topic.';
comment on column sg_public.topic.user_id
  is 'The user who created the topic.';
comment on column sg_public.topic.session_id
  is 'The logged out person who created the topic.';
comment on column sg_public.topic.name
  is 'The name of the topic.';
comment on column sg_public.topic.entity_id
  is 'The entity the topic belongs to.';
comment on column sg_public.topic.entity_kind
  is 'The kind of entity the topic belongs to.';

create index on "sg_public"."topic"("created");
create index on "sg_public"."topic"("entity_id");

create table sg_public.post (
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  user_id uuid null references sg_public.user (id)
    check (kind <> 'vote' or user_id is not null),
  session_id uuid null,
  topic_id uuid not null references sg_public.topic (id),
  kind sg_public.post_kind not null default 'post',
  body text null
    check (kind = 'vote' or body is not null),
  parent_id uuid null references sg_public.post (id)
    check (kind <> 'vote' or parent_id is not null),
  response boolean null
    check (kind <> 'vote' or response is not null),
  constraint user_or_session check (((user_id is not null) or (session_id is not null)))
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
comment on column sg_public.post.session_id
  is 'The logged out user who created the post.';
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
    references sg_public.entity_version (version_id, entity_kind),
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

create unique index post_vote_unique_idx
  on sg_public.post (user_id, parent_id)
  where kind = 'vote';

-- comment on index post_vote_unique_idx
--   is 'A user may only vote once on a proposal.';

create or replace function sg_private.verify_post()
returns trigger as $$
  declare
    parent sg_public.post;
  begin
    if (new.parent_id) then
      select * into parent
      from sg_public.post
      where id = new.parent_id;
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
    return new;
  end;
$$ language 'plpgsql';
comment on function sg_private.verify_post()
  is 'Verify valid data when creating or updating a post.';

create trigger insert_topic_user_id
  before insert on sg_public.topic
  for each row execute procedure sg_private.insert_user_or_session();
comment on trigger insert_topic_user_id on sg_public.topic
  is 'Whenever I make a new topic, auto fill the `user_id` column';

create trigger insert_post_user_id
  before insert on sg_public.post
  for each row execute procedure sg_private.insert_user_or_session();
comment on trigger insert_post_user_id on sg_public.post
  is 'Whenever I make a new post, auto fill the `user_id` column';

create trigger insert_post_verify
  before insert on sg_public.post
  for each row execute procedure sg_private.verify_post();
comment on trigger insert_post_verify on sg_public.post
  is 'Whenever I make a new post, check that the post is valid.';

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
  for insert -- any user
  with check (true);

-- Update topic: user self (name), or admin.
grant update (name) on table sg_public.topic to sg_user;
create policy update_topic on sg_public.topic
  for update to sg_user
  using (user_id = nullif(current_setting('jwt.claims.user_id', true), '')::uuid);
comment on policy update_topic on sg_public.topic
  is 'A user can update the name of their own topic.';

grant update on table sg_public.topic to sg_admin;
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
  for insert -- any user
  with check (true);

-- Update post: user self (body, response), or admin.
grant update (body, response) on table sg_public.post to sg_user;
create policy update_post on sg_public.post
  for update to sg_user
  using (user_id = nullif(current_setting('jwt.claims.user_id', true), '')::uuid);
comment on policy update_post on sg_public.post
  is 'A user can update the body or response of their own post.';

grant update on table sg_public.post to sg_admin;
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

-- Update or delete post_entity_version: admin.
grant update, delete on table sg_public.post_entity_version
  to sg_admin;

create or replace function sg_public.topic_posts(sg_public.topic)
returns setof sg_public.post as $$
  select p.*
  from sg_public.post p
  where p.topic_id = $1.id
  order by p.created desc;
$$ language sql stable;
comment on function sg_public.topic_posts(sg_public.topic)
  is 'Returns the posts of the topic.';
grant execute on function sg_public.topic_posts(sg_public.topic)
  to sg_anonymous, sg_user, sg_admin;

create index on "sg_public"."post"("created");
create index on "sg_public"."post"("user_id");


CREATE INDEX ON "sg_public"."topic"("user_id");
CREATE INDEX ON "sg_public"."post"("topic_id");
CREATE INDEX ON "sg_public"."post"("parent_id");
CREATE INDEX ON "sg_public"."post_entity_version"("version_id", "entity_kind");
CREATE INDEX ON "sg_public"."topic"("entity_id", "entity_kind");

-- migrate:down

