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

-- migrate:down

