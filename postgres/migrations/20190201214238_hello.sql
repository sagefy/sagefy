-- migrate:up

create extension if not exists "uuid-ossp";
create extension if not exists "pgcrypto";
create extension if not exists "postgres-json-schema";
create extension if not exists "pgjwt";
create extension if not exists "unaccent";

create schema sg_public;
comment on schema sg_public is 'Schema exposed to GraphQL.';

create schema sg_private;
comment on schema sg_private is 'Schema hidden from GraphQL.';

drop role if exists sg_postgraphile;
create role sg_postgraphile login password 'FIXME_064242DF1E7140E190BBC672912EE966';
comment on role sg_postgraphile is 'Access role for Postgraphile';

drop role if exists sg_anonymous;
create role sg_anonymous;
comment on role sg_anonymous is 'Anonymous role is a default logged out user.';

drop role if exists sg_user;
create role sg_user;
comment on role sg_user is 'User role is a default logged in user.';

drop role if exists sg_admin;
create role sg_admin;
comment on role sg_admin is 'Admin role can change any public facing data.';

grant sg_admin to sg_postgraphile;
grant sg_user to sg_postgraphile;
grant sg_anonymous to sg_postgraphile;

-- Disable function execution permission by default.
alter default privileges revoke execute on functions from public;

-- Allow everyone to see the sg_public schema exists.
grant usage on schema sg_public to sg_anonymous, sg_user, sg_admin;

-- migrate:down
