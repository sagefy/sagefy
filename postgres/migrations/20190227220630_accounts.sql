-- migrate:up

-- UPDATE EXISTING FUNCTIONS TO SUPPORT RESETS

alter type sg_public.jwt_token
  add attribute uniq text cascade;
comment on type sg_public.jwt_token
  is 'Create a JWT with role, user_id, session_id, and uniq.';
-- no need to update access

create or replace function sg_public.get_anonymous_token()
returns sg_public.jwt_token as $$
  select ('sg_anonymous', null, uuid_generate_v4(), null)::sg_public.jwt_token;
$$ language sql volatile;
-- no need to update comment
-- no need to update access

drop function sg_public.sign_up(text, text, text);
create or replace function sg_public.sign_up(
  name text,
  email text,
  password text
) returns sg_public.jwt_token as $$
declare
  public_user sg_public.user;
  private_user sg_private.user;
begin
  if (char_length(password) < 8) then
    raise exception 'I need at least 8 characters for passwords.'
      using errcode = '355CAC69';
  end if;
  insert into sg_public.user ("name")
    values (name)
    returning * into public_user;
  insert into sg_private.user ("user_id", "email", "password")
    values (public_user.id, email, crypt(password, gen_salt('bf', 8)))
    returning * into private_user;
  return (private_user.role, public_user.id, null, null)::sg_public.jwt_token;
end;
$$ language plpgsql strict security definer;
-- no need to update comment
grant execute on function sg_public.sign_up(text, text, text) to sg_anonymous;

-- ABLE TO LOG IN

create or replace function sg_public.log_in(
  name text,
  password text
) returns sg_public.jwt_token as $$
declare
  xu sg_private.user;
begin
  select prvu.* into xu
    from sg_private.user prvu, sg_public.user pubu
    where
      prvu.user_id = pubu.id and (
        pubu.name = $1 or -- $1 == name
        prvu.email = $1
      )
    limit 1;
  if (xu is null) then
    raise exception 'No user found.' using errcode = '4F811CFE';
  end if;
  if (xu.password = crypt(password, xu.password)) then
    return (xu.role, xu.user_id, null, null)::sg_public.jwt_token;
  else
    raise exception 'Your password didn''t match.'
      using errcode = '51EA51A9';
  end if;
end;
$$ language plpgsql strict security definer;
comment on function sg_public.log_in(text, text) is 'Logs in a single user.';
grant execute on function sg_public.log_in(text, text)
  to sg_anonymous, sg_user, sg_admin;

-- ABLE TO VERIFY

create function sg_public.get_current_user()
returns sg_public.user as $$
  select *
  from sg_public.user
  where id = current_setting('jwt.claims.user_id')::uuid
$$ language sql stable;
comment on function sg_public.get_current_user()
  is 'Get the current logged in user.';
grant execute on function sg_public.get_current_user()
  to sg_anonymous, sg_user, sg_admin;

-- ABLE TO UPDATE NAME & VIEW_SUBJECTS

create trigger update_user_modified
  before update on sg_public.user
  for each row execute procedure sg_private.update_modified_column();
comment on trigger update_user_modified on sg_public.user
  is 'Whenever the user changes, update the `modified` column.';

-- Select user: any.
grant select on table sg_public.user to sg_anonymous, sg_user, sg_admin;
create policy select_user on sg_public.user
  for select -- any user
  using (true);
comment on policy select_user on sg_public.user
  is 'Anyone can select public user data.';

-- Update user: user self (name, settings), or admin.
grant update (name, view_subjects) on table sg_public.user to sg_user, sg_admin;
create policy update_user on sg_public.user
  for update to sg_user
  using (id = current_setting('jwt.claims.user_id')::uuid);
comment on policy update_user on sg_public.user
  is 'A user can update their own public user data name and settings.';
create policy update_user_admin on sg_public.user
  for update to sg_admin
  using (true);
comment on policy update_user_admin on sg_public.user
  is 'An admin can update any public user data.';

-- Delete user: user self, or admin.
grant delete on table sg_public.user to sg_user, sg_admin;
create policy delete_user on sg_public.user
  for delete to sg_user
  using (id = current_setting('jwt.claims.user_id')::uuid);
comment on policy delete_user on sg_public.user
  is 'A user can delete their own public user data.';
create policy delete_user_admin on sg_public.user
  for delete to sg_admin
  using (true);
comment on policy delete_user_admin on sg_public.user
  is 'An admin can delete any public user data';

-- ENABLE RESET PASSWORD & EMAIL

create or replace function sg_public.send_password_token(
  email text
) returns void as $$
  declare
    xu sg_private.user;
  begin
    select * into xu
    from sg_private.user
    where sg_private.user.email = $1
    limit 1;
    if (xu is null) then
      raise exception 'No user found.' using errcode = '3883C744';
    end if;
    perform pg_notify(
      'send_password_token',
      concat(xu.email, ' ', xu.user_id::text, ' ', xu.password)
    );
  end;
$$ language plpgsql strict security definer;
comment on function sg_public.send_password_token(text)
  is 'Generate and email a token to update password.';
grant execute on function sg_public.send_password_token(text)
  to sg_anonymous, sg_user, sg_admin;

create or replace function sg_public.send_email_token(
  email text
) returns void as $$
  declare
    xu sg_private.user;
  begin
    select * into xu
    from sg_private.user
    where sg_private.user.email = $1
    limit 1;
    if (xu is null) then
      raise exception 'No user found.' using errcode = '47C88D24';
    end if;
    perform pg_notify(
      'send_email_token',
      concat(xu.email, ' ', xu.user_id::text, ' ', xu.email)
    );
  end;
$$ language plpgsql strict security definer;
comment on function sg_public.send_email_token(text)
  is 'Generate and email a token to update email.';
grant execute on function sg_public.send_email_token(text)
  to sg_anonymous, sg_user, sg_admin;

create function sg_public.update_email(
  new_email text
) returns void as $$
  declare
    xu sg_private.user;
    xuser_id uuid;
    xemail text;
    xpassword text;
  begin
    xuser_id := current_setting('jwt.claims.user_id')::uuid;
    xemail := split_part(current_setting('jwt.claims.uniq')::text, ',', 1);
    select * into xu
    from sg_private.user
    where sg_private.user.user_id = xuser_id
      and sg_private.user.email = xemail
    limit 1;
    if (xu is null) then
      raise exception 'No match found.' using errcode = '58483A61';
    end if;
    update sg_private.user
    set email = new_email
    where user_id = xuser_id;
  end;
$$ language plpgsql strict security definer;
comment on function sg_public.update_email(text)
  is 'Update the user''s email address.';
grant execute on function sg_public.update_email(text)
  to sg_anonymous, sg_user, sg_admin;

create function sg_public.update_password(
  new_password text
) returns void as $$
  declare
    xu sg_private.user;
    xuser_id uuid;
    xemail text;
    xpassword text;
  begin
    xuser_id := current_setting('jwt.claims.user_id')::uuid;
    xpassword := split_part(current_setting('jwt.claims.uniq')::text, ',', 1);
    select * into xu
    from sg_private.user
    where sg_private.user.user_id = xuser_id
      and sg_private.user.password = xpassword
    limit 1;
    if (xu is null) then
      raise exception 'No match found.' using errcode = 'EBC6E992';
    end if;
    update sg_private.user
    set password = crypt(new_password, gen_salt('bf', 8))
    where user_id = xuser_id;
  end;
$$ language plpgsql strict security definer;
comment on function sg_public.update_password(text)
  is 'Update the user''s password.';
grant execute on function sg_public.update_password(text)
  to sg_anonymous, sg_user, sg_admin;

create function sg_private.notify_update_email()
returns trigger as $$
begin
  perform pg_notify('update_email', old.email);
  return new;
end;
$$ language 'plpgsql';
comment on function sg_private.notify_update_email()
  is 'Whenever a user changes their email, email their old account.';
create trigger update_email
  after update of email on sg_private.user
  for each row execute procedure sg_private.notify_update_email();
comment on trigger create_user on sg_private.user
  is 'Whenever a user changes their email, email their old account.';

create function sg_private.notify_update_password()
returns trigger as $$
begin
  perform pg_notify('update_password', old.email);
  return new;
end;
$$ language 'plpgsql';
comment on function sg_private.notify_update_password()
  is 'Whenever a user changes their password, email them.';
create trigger update_password
  after update of password on sg_private.user
  for each row execute procedure sg_private.notify_update_password();
comment on trigger create_user on sg_private.user
  is 'Whenever a user changes their password, email them.';

-- migrate:down

