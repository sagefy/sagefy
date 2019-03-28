-- migrate:up

create or replace function sg_public.get_current_user()
returns sg_public.user as $$
  select *
  from sg_public.user
  where id = nullif(current_setting('jwt.claims.user_id', true), '')::uuid
$$ language sql stable;
comment on function sg_public.get_current_user()
  is 'Get the current logged in user.';
grant execute on function sg_public.get_current_user()
  to sg_anonymous, sg_user, sg_admin;

-- migrate:down

