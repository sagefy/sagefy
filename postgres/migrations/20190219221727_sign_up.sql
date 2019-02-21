-- migrate:up

create extension if not exists "citext";

create type sg_public.email_frequency as enum(
  'immediate',
  'daily',
  'weekly',
  'never'
);
comment on type sg_public.email_frequency
  is 'Email frequency options per user';

create type sg_public.user_role as enum(
  'sg_anonymous',
  'sg_user',
  'sg_admin'
);
comment on type sg_public.user_role
  is 'User role options.';

create table sg_public.user (
  id uuid primary key default uuid_generate_v4(),
  created timestamp not null default current_timestamp,
  modified timestamp not null default current_timestamp,
  name citext not null unique,
  view_subjects boolean not null default false
);

comment on table sg_public.user
  is 'The public user data table. Anyone can see this data.';
comment on column sg_public.user.id
  is 'The primary key of the user.';
comment on column sg_public.user.created
  is 'When the user signed up.';
comment on column sg_public.user.modified
  is 'When the public user data updated last.';
comment on column sg_public.user.name
  is 'The user''s name or username';
comment on column sg_public.user.view_subjects
  is 'Public setting for if the user wants to display what they are learning.';

create table sg_private.user (
  user_id uuid primary key references sg_public.user (id) on delete cascade,
  email citext not null unique
    constraint email_check check (email ~* '^\S+@\S+\.\S+$'),
  password varchar(60) not null
    constraint pass_check check (password ~* '^\$2\w\$.*$'),
  role sg_public.user_role not null default 'sg_user',
  email_frequency sg_public.email_frequency not null default 'immediate'
);

comment on table sg_private.user
  is 'Private user data -- this should be highly protected.';
comment on column sg_private.user.email
  is 'The user''s private email address -- for notices and password resets.';
comment on column sg_private.user.password
  is 'The bcrypt hash of the user''s password.';
comment on column sg_private.user.role
  is 'The role of the user, `sg_user` or `sg_admin`.';
comment on column sg_private.user.email_frequency
  is 'Setting of how often the user would like to receive notice emails.';
comment on constraint email_check on sg_private.user
  is 'An email must match the email format `a@b.c`.';
comment on constraint pass_check on sg_private.user
  is 'A password must batch the bcrypt hash format '
     '`$2w$...`, where w is a, b, or y.';

create function sg_public.sign_up(
  name text,
  email text,
  password text
) returns sg_public.user as $$
declare
  xuser sg_public.user;
begin
  if (char_length(password) < 8) then
    raise exception 'I need at least 8 characters for passwords.'
      using errcode = '355CAC69';
  end if;
  insert into sg_public.user ("name")
    values (name)
    returning * into xuser;
  insert into sg_private.user ("user_id", "email", "password")
    values (xuser.id, email, crypt(password, gen_salt('bf', 8)));
  return xuser;
end;
$$ language plpgsql strict security definer;
comment on function sg_public.sign_up(text, text, text)
  is 'Signs up a single user.';

create function sg_private.notify_create_user()
returns trigger as $$
begin
  perform pg_notify('create_user', new.email);
  return new;
end;
$$ language plpgsql strict security definer;
comment on function sg_private.notify_create_user()
  is 'Whenever a new user signs up, email them.';

create trigger create_user
  after insert on sg_private.user
  for each row execute procedure sg_private.notify_create_user();
comment on trigger create_user on sg_private.user
  is 'Whenever a new user signs up, email them.';

-- Enable RLS.
alter table sg_public.user enable row level security;

-- Insert user: only anonymous, via function.
grant execute on function sg_public.sign_up(text, text, text) to sg_anonymous;

-- migrate:down

