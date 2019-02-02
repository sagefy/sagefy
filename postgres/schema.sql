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
-- Name: follow_suggest(); Type: FUNCTION; Schema: sg_private; Owner: -
--

CREATE FUNCTION sg_private.follow_suggest() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
  begin
    insert into sg_public.suggest_follow
    (suggest_id, user_id, session_id)
    values
    (new.id,
      current_setting('jwt.claims.user_id')::uuid,
      current_setting('jwt.claims.session_id')::uuid);
  end;
$$;


--
-- Name: FUNCTION follow_suggest(); Type: COMMENT; Schema: sg_private; Owner: -
--

COMMENT ON FUNCTION sg_private.follow_suggest() IS 'Follow a given suggest';


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
-- Name: schema_migrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.schema_migrations (
    version character varying(255) NOT NULL
);


--
-- Name: suggest; Type: TABLE; Schema: sg_public; Owner: -
--

CREATE TABLE sg_public.suggest (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    created timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    modified timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    name text NOT NULL,
    body text NOT NULL
);


--
-- Name: TABLE suggest; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TABLE sg_public.suggest IS 'A suggestion for a new subject in Sagefy.';


--
-- Name: COLUMN suggest.id; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.suggest.id IS 'The ID of the suggest.';


--
-- Name: COLUMN suggest.created; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.suggest.created IS 'When the user created the suggest.';


--
-- Name: COLUMN suggest.modified; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.suggest.modified IS 'When someone last changed the suggest.';


--
-- Name: COLUMN suggest.name; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.suggest.name IS 'The name of the suggested subject.';


--
-- Name: COLUMN suggest.body; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.suggest.body IS 'The description and goals of the suggested subject.';


--
-- Name: suggest_follow; Type: TABLE; Schema: sg_public; Owner: -
--

CREATE TABLE sg_public.suggest_follow (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    created timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    modified timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    suggest_id uuid NOT NULL,
    session_id uuid NOT NULL
);


--
-- Name: TABLE suggest_follow; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TABLE sg_public.suggest_follow IS 'A relationship between a suggest and a user.';


--
-- Name: COLUMN suggest_follow.id; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.suggest_follow.id IS 'The ID of the suggest follow.';


--
-- Name: COLUMN suggest_follow.created; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.suggest_follow.created IS 'When the user followed the suggest.';


--
-- Name: COLUMN suggest_follow.modified; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.suggest_follow.modified IS 'When the relationship last changed.';


--
-- Name: COLUMN suggest_follow.suggest_id; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.suggest_follow.suggest_id IS 'The suggest the user is following.';


--
-- Name: COLUMN suggest_follow.session_id; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.suggest_follow.session_id IS 'The session ID of the user.';


--
-- Name: schema_migrations schema_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.schema_migrations
    ADD CONSTRAINT schema_migrations_pkey PRIMARY KEY (version);


--
-- Name: suggest_follow suggest_follow_pkey; Type: CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.suggest_follow
    ADD CONSTRAINT suggest_follow_pkey PRIMARY KEY (id);


--
-- Name: suggest_follow suggest_follow_suggest_id_session_id_key; Type: CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.suggest_follow
    ADD CONSTRAINT suggest_follow_suggest_id_session_id_key UNIQUE (suggest_id, session_id);


--
-- Name: suggest suggest_pkey; Type: CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.suggest
    ADD CONSTRAINT suggest_pkey PRIMARY KEY (id);


--
-- Name: suggest insert_suggest_then_follow; Type: TRIGGER; Schema: sg_public; Owner: -
--

CREATE TRIGGER insert_suggest_then_follow AFTER INSERT ON sg_public.suggest FOR EACH ROW EXECUTE PROCEDURE sg_private.follow_suggest();


--
-- Name: TRIGGER insert_suggest_then_follow ON suggest; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TRIGGER insert_suggest_then_follow ON sg_public.suggest IS 'Whenever I create a suggest, immediately follow the suggest';


--
-- Name: suggest_follow update_suggest_follow_modified; Type: TRIGGER; Schema: sg_public; Owner: -
--

CREATE TRIGGER update_suggest_follow_modified BEFORE UPDATE ON sg_public.suggest_follow FOR EACH ROW EXECUTE PROCEDURE sg_private.update_modified_column();


--
-- Name: TRIGGER update_suggest_follow_modified ON suggest_follow; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TRIGGER update_suggest_follow_modified ON sg_public.suggest_follow IS 'Whenever a suggest follow changes, update the `modified` column.';


--
-- Name: suggest update_suggest_modified; Type: TRIGGER; Schema: sg_public; Owner: -
--

CREATE TRIGGER update_suggest_modified BEFORE UPDATE ON sg_public.suggest FOR EACH ROW EXECUTE PROCEDURE sg_private.update_modified_column();


--
-- Name: TRIGGER update_suggest_modified ON suggest; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TRIGGER update_suggest_modified ON sg_public.suggest IS 'Whenever a suggest changes, update the `modified` column.';


--
-- Name: suggest_follow suggest_follow_suggest_id_fkey; Type: FK CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.suggest_follow
    ADD CONSTRAINT suggest_follow_suggest_id_fkey FOREIGN KEY (suggest_id) REFERENCES sg_public.suggest(id);


--
-- PostgreSQL database dump complete
--


--
-- Dbmate schema migrations
--

INSERT INTO public.schema_migrations (version) VALUES
    ('20190201214238'),
    ('20190201220821');
