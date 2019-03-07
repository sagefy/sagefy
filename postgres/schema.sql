SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: sg_private; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA sg_private;


--
-- Name: SCHEMA sg_private; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON SCHEMA sg_private IS 'Schema hidden from GraphQL.';


--
-- Name: sg_public; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA sg_public;


--
-- Name: SCHEMA sg_public; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON SCHEMA sg_public IS 'Schema exposed to GraphQL.';


--
-- Name: citext; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS citext WITH SCHEMA public;


--
-- Name: EXTENSION citext; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION citext IS 'data type for case-insensitive character strings';


--
-- Name: pgcrypto; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;


--
-- Name: EXTENSION pgcrypto; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION pgcrypto IS 'cryptographic functions';


--
-- Name: postgres-json-schema; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS "postgres-json-schema" WITH SCHEMA public;


--
-- Name: EXTENSION "postgres-json-schema"; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION "postgres-json-schema" IS 'Validate JSON schemas';


--
-- Name: unaccent; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS unaccent WITH SCHEMA public;


--
-- Name: EXTENSION unaccent; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION unaccent IS 'text search dictionary that removes accents';


--
-- Name: uuid-ossp; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;


--
-- Name: EXTENSION "uuid-ossp"; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';


--
-- Name: email_frequency; Type: TYPE; Schema: sg_public; Owner: -
--

CREATE TYPE sg_public.email_frequency AS ENUM (
    'immediate',
    'daily',
    'weekly',
    'never'
);


--
-- Name: TYPE email_frequency; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TYPE sg_public.email_frequency IS 'Email frequency options per user';


--
-- Name: jwt_token; Type: TYPE; Schema: sg_public; Owner: -
--

CREATE TYPE sg_public.jwt_token AS (
	role text,
	user_id uuid,
	session_id uuid,
	uniq text
);


--
-- Name: TYPE jwt_token; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TYPE sg_public.jwt_token IS 'Create a JWT with role, user_id, session_id, and uniq.';


--
-- Name: user_role; Type: TYPE; Schema: sg_public; Owner: -
--

CREATE TYPE sg_public.user_role AS ENUM (
    'sg_anonymous',
    'sg_user',
    'sg_admin'
);


--
-- Name: TYPE user_role; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TYPE sg_public.user_role IS 'User role options.';


--
-- Name: notify_create_user(); Type: FUNCTION; Schema: sg_private; Owner: -
--

CREATE FUNCTION sg_private.notify_create_user() RETURNS trigger
    LANGUAGE plpgsql STRICT SECURITY DEFINER
    AS $$
begin
  perform pg_notify('create_user', new.email);
  return new;
end;
$$;


--
-- Name: FUNCTION notify_create_user(); Type: COMMENT; Schema: sg_private; Owner: -
--

COMMENT ON FUNCTION sg_private.notify_create_user() IS 'Whenever a new user signs up, email them.';


--
-- Name: notify_update_email(); Type: FUNCTION; Schema: sg_private; Owner: -
--

CREATE FUNCTION sg_private.notify_update_email() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin
  perform pg_notify('update_email', old.email);
  return new;
end;
$$;


--
-- Name: FUNCTION notify_update_email(); Type: COMMENT; Schema: sg_private; Owner: -
--

COMMENT ON FUNCTION sg_private.notify_update_email() IS 'Whenever a user changes their email, email their old account.';


--
-- Name: notify_update_password(); Type: FUNCTION; Schema: sg_private; Owner: -
--

CREATE FUNCTION sg_private.notify_update_password() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin
  perform pg_notify('update_password', old.email);
  return new;
end;
$$;


--
-- Name: FUNCTION notify_update_password(); Type: COMMENT; Schema: sg_private; Owner: -
--

COMMENT ON FUNCTION sg_private.notify_update_password() IS 'Whenever a user changes their password, email them.';


--
-- Name: trim_user_email(); Type: FUNCTION; Schema: sg_private; Owner: -
--

CREATE FUNCTION sg_private.trim_user_email() RETURNS trigger
    LANGUAGE plpgsql STRICT SECURITY DEFINER
    AS $$
begin
  new.email = trim(new.email);
  return new;
end;
$$;


--
-- Name: FUNCTION trim_user_email(); Type: COMMENT; Schema: sg_private; Owner: -
--

COMMENT ON FUNCTION sg_private.trim_user_email() IS 'Trim the user''s email.';


--
-- Name: trim_user_name(); Type: FUNCTION; Schema: sg_private; Owner: -
--

CREATE FUNCTION sg_private.trim_user_name() RETURNS trigger
    LANGUAGE plpgsql STRICT SECURITY DEFINER
    AS $$
begin
  new.name = trim(new.name);
  return new;
end;
$$;


--
-- Name: FUNCTION trim_user_name(); Type: COMMENT; Schema: sg_private; Owner: -
--

COMMENT ON FUNCTION sg_private.trim_user_name() IS 'Trim the user''s name.';


--
-- Name: update_modified_column(); Type: FUNCTION; Schema: sg_private; Owner: -
--

CREATE FUNCTION sg_private.update_modified_column() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin new.modified = now();
  return new;
end;
$$;


--
-- Name: FUNCTION update_modified_column(); Type: COMMENT; Schema: sg_private; Owner: -
--

COMMENT ON FUNCTION sg_private.update_modified_column() IS 'Whenever the row changes, update the `modified` column.';


--
-- Name: get_anonymous_token(); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.get_anonymous_token() RETURNS sg_public.jwt_token
    LANGUAGE sql
    AS $$
  select ('sg_anonymous', null, uuid_generate_v4(), null)::sg_public.jwt_token;
$$;


--
-- Name: FUNCTION get_anonymous_token(); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public.get_anonymous_token() IS 'Create anonymous user token.';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: user; Type: TABLE; Schema: sg_public; Owner: -
--

CREATE TABLE sg_public."user" (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    created timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    modified timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    name public.citext NOT NULL,
    view_subjects boolean DEFAULT false NOT NULL
);


--
-- Name: TABLE "user"; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TABLE sg_public."user" IS 'The public user data table. Anyone can see this data.';


--
-- Name: COLUMN "user".id; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public."user".id IS 'The primary key of the user.';


--
-- Name: COLUMN "user".created; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public."user".created IS 'When the user signed up.';


--
-- Name: COLUMN "user".modified; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public."user".modified IS 'When the public user data updated last.';


--
-- Name: COLUMN "user".name; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public."user".name IS 'The user''s name or username';


--
-- Name: COLUMN "user".view_subjects; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public."user".view_subjects IS 'Public setting for if the user wants to display what they are learning.';


--
-- Name: get_current_user(); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.get_current_user() RETURNS sg_public."user"
    LANGUAGE sql STABLE
    AS $$
  select *
  from sg_public.user
  where id = current_setting('jwt.claims.user_id')::uuid
$$;


--
-- Name: FUNCTION get_current_user(); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public.get_current_user() IS 'Get the current logged in user.';


--
-- Name: log_in(text, text); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.log_in(name text, password text) RETURNS sg_public.jwt_token
    LANGUAGE plpgsql STRICT SECURITY DEFINER
    AS $_$
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
$_$;


--
-- Name: FUNCTION log_in(name text, password text); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public.log_in(name text, password text) IS 'Logs in a single user.';


--
-- Name: send_email_token(text); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.send_email_token(email text) RETURNS void
    LANGUAGE plpgsql STRICT SECURITY DEFINER
    AS $_$
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
$_$;


--
-- Name: FUNCTION send_email_token(email text); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public.send_email_token(email text) IS 'Generate and email a token to update email.';


--
-- Name: send_password_token(text); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.send_password_token(email text) RETURNS void
    LANGUAGE plpgsql STRICT SECURITY DEFINER
    AS $_$
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
$_$;


--
-- Name: FUNCTION send_password_token(email text); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public.send_password_token(email text) IS 'Generate and email a token to update password.';


--
-- Name: sign_up(text, text, text); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.sign_up(name text, email text, password text) RETURNS sg_public.jwt_token
    LANGUAGE plpgsql STRICT SECURITY DEFINER
    AS $$
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
$$;


--
-- Name: update_email(text); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.update_email(new_email text) RETURNS void
    LANGUAGE plpgsql STRICT SECURITY DEFINER
    AS $$
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
$$;


--
-- Name: FUNCTION update_email(new_email text); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public.update_email(new_email text) IS 'Update the user''s email address.';


--
-- Name: update_password(text); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.update_password(new_password text) RETURNS void
    LANGUAGE plpgsql STRICT SECURITY DEFINER
    AS $$
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
$$;


--
-- Name: FUNCTION update_password(new_password text); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public.update_password(new_password text) IS 'Update the user''s password.';


--
-- Name: schema_migrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.schema_migrations (
    version character varying(255) NOT NULL
);


--
-- Name: user; Type: TABLE; Schema: sg_private; Owner: -
--

CREATE TABLE sg_private."user" (
    user_id uuid NOT NULL,
    email public.citext NOT NULL,
    password character varying(60) NOT NULL,
    role sg_public.user_role DEFAULT 'sg_user'::sg_public.user_role NOT NULL,
    email_frequency sg_public.email_frequency DEFAULT 'immediate'::sg_public.email_frequency NOT NULL,
    CONSTRAINT email_check CHECK ((email OPERATOR(public.~*) '^\S+@\S+\.\S+$'::public.citext)),
    CONSTRAINT pass_check CHECK (((password)::text ~* '^\$2\w\$.*$'::text))
);


--
-- Name: TABLE "user"; Type: COMMENT; Schema: sg_private; Owner: -
--

COMMENT ON TABLE sg_private."user" IS 'Private user data -- this should be highly protected.';


--
-- Name: COLUMN "user".email; Type: COMMENT; Schema: sg_private; Owner: -
--

COMMENT ON COLUMN sg_private."user".email IS 'The user''s private email address -- for notices and password resets.';


--
-- Name: COLUMN "user".password; Type: COMMENT; Schema: sg_private; Owner: -
--

COMMENT ON COLUMN sg_private."user".password IS 'The bcrypt hash of the user''s password.';


--
-- Name: COLUMN "user".role; Type: COMMENT; Schema: sg_private; Owner: -
--

COMMENT ON COLUMN sg_private."user".role IS 'The role of the user, `sg_user` or `sg_admin`.';


--
-- Name: COLUMN "user".email_frequency; Type: COMMENT; Schema: sg_private; Owner: -
--

COMMENT ON COLUMN sg_private."user".email_frequency IS 'Setting of how often the user would like to receive notice emails.';


--
-- Name: CONSTRAINT email_check ON "user"; Type: COMMENT; Schema: sg_private; Owner: -
--

COMMENT ON CONSTRAINT email_check ON sg_private."user" IS 'An email must match the email format `a@b.c`.';


--
-- Name: CONSTRAINT pass_check ON "user"; Type: COMMENT; Schema: sg_private; Owner: -
--

COMMENT ON CONSTRAINT pass_check ON sg_private."user" IS 'A password must batch the bcrypt hash format `$2w$...`, where w is a, b, or y.';


--
-- Name: schema_migrations schema_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.schema_migrations
    ADD CONSTRAINT schema_migrations_pkey PRIMARY KEY (version);


--
-- Name: user user_email_key; Type: CONSTRAINT; Schema: sg_private; Owner: -
--

ALTER TABLE ONLY sg_private."user"
    ADD CONSTRAINT user_email_key UNIQUE (email);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: sg_private; Owner: -
--

ALTER TABLE ONLY sg_private."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (user_id);


--
-- Name: user user_name_key; Type: CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public."user"
    ADD CONSTRAINT user_name_key UNIQUE (name);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: user create_user; Type: TRIGGER; Schema: sg_private; Owner: -
--

CREATE TRIGGER create_user AFTER INSERT ON sg_private."user" FOR EACH ROW EXECUTE PROCEDURE sg_private.notify_create_user();


--
-- Name: TRIGGER create_user ON "user"; Type: COMMENT; Schema: sg_private; Owner: -
--

COMMENT ON TRIGGER create_user ON sg_private."user" IS 'Whenever a user changes their password, email them.';


--
-- Name: user trim_user_email; Type: TRIGGER; Schema: sg_private; Owner: -
--

CREATE TRIGGER trim_user_email BEFORE INSERT ON sg_private."user" FOR EACH ROW EXECUTE PROCEDURE sg_private.trim_user_email();


--
-- Name: TRIGGER trim_user_email ON "user"; Type: COMMENT; Schema: sg_private; Owner: -
--

COMMENT ON TRIGGER trim_user_email ON sg_private."user" IS 'Trim the user''s email.';


--
-- Name: user update_email; Type: TRIGGER; Schema: sg_private; Owner: -
--

CREATE TRIGGER update_email AFTER UPDATE OF email ON sg_private."user" FOR EACH ROW EXECUTE PROCEDURE sg_private.notify_update_email();


--
-- Name: user update_password; Type: TRIGGER; Schema: sg_private; Owner: -
--

CREATE TRIGGER update_password AFTER UPDATE OF password ON sg_private."user" FOR EACH ROW EXECUTE PROCEDURE sg_private.notify_update_password();


--
-- Name: user trim_user_name; Type: TRIGGER; Schema: sg_public; Owner: -
--

CREATE TRIGGER trim_user_name BEFORE INSERT ON sg_public."user" FOR EACH ROW EXECUTE PROCEDURE sg_private.trim_user_name();


--
-- Name: TRIGGER trim_user_name ON "user"; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TRIGGER trim_user_name ON sg_public."user" IS 'Trim the user''s name.';


--
-- Name: user update_user_modified; Type: TRIGGER; Schema: sg_public; Owner: -
--

CREATE TRIGGER update_user_modified BEFORE UPDATE ON sg_public."user" FOR EACH ROW EXECUTE PROCEDURE sg_private.update_modified_column();


--
-- Name: TRIGGER update_user_modified ON "user"; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TRIGGER update_user_modified ON sg_public."user" IS 'Whenever the user changes, update the `modified` column.';


--
-- Name: user user_user_id_fkey; Type: FK CONSTRAINT; Schema: sg_private; Owner: -
--

ALTER TABLE ONLY sg_private."user"
    ADD CONSTRAINT user_user_id_fkey FOREIGN KEY (user_id) REFERENCES sg_public."user"(id) ON DELETE CASCADE;


--
-- Name: user delete_user; Type: POLICY; Schema: sg_public; Owner: -
--

CREATE POLICY delete_user ON sg_public."user" FOR DELETE TO sg_user USING ((id = (current_setting('jwt.claims.user_id'::text))::uuid));


--
-- Name: user delete_user_admin; Type: POLICY; Schema: sg_public; Owner: -
--

CREATE POLICY delete_user_admin ON sg_public."user" FOR DELETE TO sg_admin USING (true);


--
-- Name: user select_user; Type: POLICY; Schema: sg_public; Owner: -
--

CREATE POLICY select_user ON sg_public."user" FOR SELECT USING (true);


--
-- Name: user update_user; Type: POLICY; Schema: sg_public; Owner: -
--

CREATE POLICY update_user ON sg_public."user" FOR UPDATE TO sg_user USING ((id = (current_setting('jwt.claims.user_id'::text))::uuid));


--
-- Name: user update_user_admin; Type: POLICY; Schema: sg_public; Owner: -
--

CREATE POLICY update_user_admin ON sg_public."user" FOR UPDATE TO sg_admin USING (true);


--
-- Name: user; Type: ROW SECURITY; Schema: sg_public; Owner: -
--

ALTER TABLE sg_public."user" ENABLE ROW LEVEL SECURITY;

--
-- PostgreSQL database dump complete
--


--
-- Dbmate schema migrations
--

INSERT INTO public.schema_migrations (version) VALUES
    ('20190201214238'),
    ('20190201220821'),
    ('20190219221727'),
    ('20190227220630');
