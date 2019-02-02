-- migrate:up

create or replace function sg_private.update_modified_column()
returns trigger as $$
begin new.modified = now();
  return new;
end;
$$ language 'plpgsql';
comment on function sg_private.update_modified_column()
  is 'Whenever the row changes, update the `modified` column.';

create type sg_public.jwt_token as (
  role text,
  user_id uuid,
  session_id uuid
);
comment on type sg_public.jwt_token
  is 'Create a JWT with role, user_id, and session_id.';

create function sg_public.get_anonymous_token()
returns sg_public.jwt_token as $$
  select ('sg_anonymous', null, uuid_generate_v4())::sg_public.jwt_token;
$$ language sql;
comment on function sg_public.get_anonymous_token() is 'Create anonymous user token.';

grant execute on function sg_public.get_anonymous_token() to sg_anonymous;

create table sg_public.suggest (
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  name text not null,
  body text not null
);

comment on table sg_public.suggest
  is 'A suggestion for a new subject in Sagefy.';
comment on column sg_public.suggest.id
  is 'The ID of the suggest.';
comment on column sg_public.suggest.created
  is 'When the user created the suggest.';
comment on column sg_public.suggest.modified
  is 'When someone last changed the suggest.';
comment on column sg_public.suggest.name
  is 'The name of the suggested subject.';
comment on column sg_public.suggest.body
  is 'The description and goals of the suggested subject.';

create table sg_public.suggest_follow (
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  suggest_id uuid not null references sg_public.suggest (id),
  -- user_id uuid null references sg_public.user (id) on delete cascade,
  session_id uuid not null,
  -- check (user_id is not null or session_id is not null),
  -- unique (suggest_id, user_id),
  unique (suggest_id, session_id)
);

comment on table sg_public.suggest_follow
  is 'A relationship between a suggest and a user.';
comment on column sg_public.suggest_follow.id
  is 'The ID of the suggest follow.';
comment on column sg_public.suggest_follow.created
  is 'When the user followed the suggest.';
comment on column sg_public.suggest_follow.modified
  is 'When the relationship last changed.';
comment on column sg_public.suggest_follow.suggest_id
  is 'The suggest the user is following.';
comment on column sg_public.suggest_follow.session_id
  is 'The session ID of the user.';

create function sg_private.follow_suggest()
returns trigger as $$
  begin
    insert into sg_public.suggest_follow
    (suggest_id, user_id, session_id)
    values
    (new.id,
      current_setting('jwt.claims.user_id')::uuid,
      current_setting('jwt.claims.session_id')::uuid);
  end;
$$ language 'plpgsql';
comment on function sg_private.follow_suggest()
  is 'Follow a given suggest';

create trigger insert_suggest_then_follow
  after insert on sg_public.suggest
  for each row execute procedure sg_private.follow_suggest();
comment on trigger insert_suggest_then_follow on sg_public.suggest
  is 'Whenever I create a suggest, immediately follow the suggest';

create trigger update_suggest_modified
  before update on sg_public.suggest
  for each row execute procedure sg_private.update_modified_column();
comment on trigger update_suggest_modified on sg_public.suggest
  is 'Whenever a suggest changes, update the `modified` column.';

create trigger update_suggest_follow_modified
  before update on sg_public.suggest_follow
  for each row execute procedure sg_private.update_modified_column();
comment on trigger update_suggest_follow_modified on sg_public.suggest_follow
  is 'Whenever a suggest follow changes, update the `modified` column.';

grant select on table sg_public.suggest to sg_anonymous, sg_user, sg_admin;
grant insert (name, body) on table sg_public.suggest
  to sg_anonymous, sg_user, sg_admin;
grant select on table sg_public.suggest_follow
  to sg_anonymous, sg_user, sg_admin;
grant insert (suggest_id) on table sg_public.suggest_follow
  to sg_anonymous, sg_user, sg_admin;

-- migrate:down

