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
-- Name: pgcrypto; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;


--
-- Name: EXTENSION pgcrypto; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION pgcrypto IS 'cryptographic functions';


--
-- Name: pgjwt; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pgjwt WITH SCHEMA public;


--
-- Name: EXTENSION pgjwt; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION pgjwt IS 'JSON Web Token API for Postgresql';


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
	session_id uuid
);


--
-- Name: TYPE jwt_token; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TYPE sg_public.jwt_token IS 'Create a JWT with role, user_id, and session_id.';


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
  select ('sg_anonymous', null, uuid_generate_v4())::sg_public.jwt_token;
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
    name text NOT NULL,
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
-- Name: sign_up(text, text, text); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.sign_up(name text, email text, password text) RETURNS sg_public."user"
    LANGUAGE plpgsql STRICT SECURITY DEFINER
    AS $$
declare
  xuser sg_public.user;
begin
  insert into sg_public.user ("name")
    values (name)
    returning * into xuser;
  insert into sg_private.user ("user_id", "email", "password")
    values (xuser.id, email, crypt(password, gen_salt('bf', 8)));
  return xuser;
end;
$$;


--
-- Name: FUNCTION sign_up(name text, email text, password text); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public.sign_up(name text, email text, password text) IS 'Signs up a single user.';


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
    email text NOT NULL,
    password character varying(60) NOT NULL,
    role sg_public.user_role DEFAULT 'sg_user'::sg_public.user_role NOT NULL,
    email_frequency sg_public.email_frequency DEFAULT 'immediate'::sg_public.email_frequency NOT NULL,
    CONSTRAINT email_check CHECK ((email ~* '^\S+@\S+\.\S+$'::text)),
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

COMMENT ON TRIGGER create_user ON sg_private."user" IS 'Whenever a new user signs up, email them.';


--
-- Name: user user_user_id_fkey; Type: FK CONSTRAINT; Schema: sg_private; Owner: -
--

ALTER TABLE ONLY sg_private."user"
    ADD CONSTRAINT user_user_id_fkey FOREIGN KEY (user_id) REFERENCES sg_public."user"(id) ON DELETE CASCADE;


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
    ('20190219221727');
