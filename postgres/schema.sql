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
-- Name: card_kind; Type: TYPE; Schema: sg_public; Owner: -
--

CREATE TYPE sg_public.card_kind AS ENUM (
    'video',
    'page',
    'unscored_embed',
    'choice'
);


--
-- Name: TYPE card_kind; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TYPE sg_public.card_kind IS 'The kinds of cards available to learn. Expanding.';


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
-- Name: entity_kind; Type: TYPE; Schema: sg_public; Owner: -
--

CREATE TYPE sg_public.entity_kind AS ENUM (
    'card',
    'subject'
);


--
-- Name: TYPE entity_kind; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TYPE sg_public.entity_kind IS 'The types of learning entities.';


--
-- Name: entity_status; Type: TYPE; Schema: sg_public; Owner: -
--

CREATE TYPE sg_public.entity_status AS ENUM (
    'pending',
    'blocked',
    'declined',
    'accepted'
);


--
-- Name: TYPE entity_status; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TYPE sg_public.entity_status IS 'The four statuses of entity versions.';


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
-- Name: insert_user_or_session(); Type: FUNCTION; Schema: sg_private; Owner: -
--

CREATE FUNCTION sg_private.insert_user_or_session() RETURNS trigger
    LANGUAGE plpgsql STRICT SECURITY DEFINER
    AS $$
begin
  if (current_setting('jwt.claims.user_id') is not null
      and current_setting('jwt.claims.user_id') <> '') then
    new.user_id = current_setting('jwt.claims.user_id')::uuid;
  elsif (current_setting('jwt.claims.session_id') is not null
      and current_setting('jwt.claims.session_id') <> '') then
    new.session_id = current_setting('jwt.claims.session_id')::uuid;
  end if;
  return new;
end;
$$;


--
-- Name: FUNCTION insert_user_or_session(); Type: COMMENT; Schema: sg_private; Owner: -
--

COMMENT ON FUNCTION sg_private.insert_user_or_session() IS 'When inserting a row, automatically set the `user_id` or `session_id` field.';


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
        pubu.name = trim($1) or -- $1 == name
        prvu.email = trim($1)
      )
    limit 1;
  if (xu is null) then
    raise exception 'No user found.' using errcode = '4F811CFE';
  end if;
  if (xu.password = crypt(trim(password), xu.password)) then
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
-- Name: card_version; Type: TABLE; Schema: sg_public; Owner: -
--

CREATE TABLE sg_public.card_version (
    version_id uuid NOT NULL,
    created timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    modified timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    entity_id uuid NOT NULL,
    previous_id uuid,
    language character varying(5) DEFAULT 'en'::character varying NOT NULL,
    name text NOT NULL,
    status sg_public.entity_status DEFAULT 'pending'::sg_public.entity_status NOT NULL,
    available boolean DEFAULT true NOT NULL,
    tags text[] DEFAULT ARRAY[]::text[],
    user_id uuid,
    session_id uuid,
    subject_id uuid NOT NULL,
    kind sg_public.card_kind NOT NULL,
    data jsonb NOT NULL,
    CONSTRAINT lang_check CHECK (((language)::text ~* '^\w{2}(-\w{2})?$'::text)),
    CONSTRAINT user_or_session CHECK (((user_id IS NOT NULL) OR (session_id IS NOT NULL))),
    CONSTRAINT valid_choice_card CHECK (((kind <> 'choice'::sg_public.card_kind) OR public.validate_json_schema('{"type": "object", "required": ["body", "options", "max_options_to_show"], "properties": {"body": {"type": "string"}, "options": {"type": "object", "minProperties": 1, "patternProperties": {"^[a-zA-Z0-9-]+$": {"type": "object", "required": ["value", "correct", "feedback"], "properties": {"value": {"type": "string"}, "correct": {"type": "boolean"}, "feedback": {"type": "string"}}}}, "additionalProperties": false}, "max_options_to_show": {"type": "integer", "default": 4, "minimum": 2}}}'::jsonb, data))),
    CONSTRAINT valid_page_card CHECK (((kind <> 'page'::sg_public.card_kind) OR public.validate_json_schema('{"type": "object", "required": ["body"], "properties": {"body": {"type": "string"}}}'::jsonb, data))),
    CONSTRAINT valid_unscored_embed_card CHECK (((kind <> 'unscored_embed'::sg_public.card_kind) OR public.validate_json_schema('{"type": "object", "required": ["url"], "properties": {"url": {"type": "string", "format": "uri"}}}'::jsonb, data))),
    CONSTRAINT valid_video_card CHECK (((kind <> 'video'::sg_public.card_kind) OR public.validate_json_schema('{"type": "object", "required": ["site", "video_id"], "properties": {"site": {"enum": ["youtube", "vimeo"], "type": "string"}, "video_id": {"type": "string"}}}'::jsonb, data)))
);


--
-- Name: TABLE card_version; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TABLE sg_public.card_version IS 'Every version of the cards. A card is a single learning activity. A card belongs to a single subject.';


--
-- Name: COLUMN card_version.version_id; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.card_version.version_id IS 'The version ID -- a single card can have many versions.';


--
-- Name: COLUMN card_version.created; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.card_version.created IS 'When a user created this version.';


--
-- Name: COLUMN card_version.modified; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.card_version.modified IS 'When a user last modified this version.';


--
-- Name: COLUMN card_version.entity_id; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.card_version.entity_id IS 'The overall entity ID.';


--
-- Name: COLUMN card_version.previous_id; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.card_version.previous_id IS 'The previous version this version is based on.';


--
-- Name: COLUMN card_version.language; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.card_version.language IS 'Which human language this card contains.';


--
-- Name: COLUMN card_version.name; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.card_version.name IS 'The name of the card.';


--
-- Name: COLUMN card_version.status; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.card_version.status IS 'The status of the card. The latest accepted version is current.';


--
-- Name: COLUMN card_version.available; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.card_version.available IS 'Whether the card is available to learners.';


--
-- Name: COLUMN card_version.tags; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.card_version.tags IS 'A list of tags. Think Bloom taxonomy.';


--
-- Name: COLUMN card_version.user_id; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.card_version.user_id IS 'Which user created this version.';


--
-- Name: COLUMN card_version.session_id; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.card_version.session_id IS 'If no user, which session created this version.';


--
-- Name: COLUMN card_version.subject_id; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.card_version.subject_id IS 'The subject the card belongs to.';


--
-- Name: COLUMN card_version.kind; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.card_version.kind IS 'The subkind of the card, such as video or choice.';


--
-- Name: COLUMN card_version.data; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.card_version.data IS 'The data of the card. The card kind changes the data shape.';


--
-- Name: CONSTRAINT lang_check ON card_version; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON CONSTRAINT lang_check ON sg_public.card_version IS 'Languages must be BCP47 compliant.';


--
-- Name: CONSTRAINT user_or_session ON card_version; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON CONSTRAINT user_or_session ON sg_public.card_version IS 'Ensure only the user or session has data.';


--
-- Name: CONSTRAINT valid_choice_card ON card_version; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON CONSTRAINT valid_choice_card ON sg_public.card_version IS 'If the `kind` is `choice`, ensure `data` matches the data shape.';


--
-- Name: CONSTRAINT valid_page_card ON card_version; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON CONSTRAINT valid_page_card ON sg_public.card_version IS 'If the `kind` is `page`, ensure `data` matches the data shape.';


--
-- Name: CONSTRAINT valid_unscored_embed_card ON card_version; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON CONSTRAINT valid_unscored_embed_card ON sg_public.card_version IS 'If the `kind` is `unscored_embed`, ensure `data` matches the data shape.';


--
-- Name: CONSTRAINT valid_video_card ON card_version; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON CONSTRAINT valid_video_card ON sg_public.card_version IS 'If the `kind` is `video`, ensure `data` matches the data shape.';


--
-- Name: new_card(character varying, text, text[], uuid, sg_public.card_kind, jsonb); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.new_card(language character varying, name text, tags text[], subject_id uuid, kind sg_public.card_kind, data jsonb) RETURNS sg_public.card_version
    LANGUAGE plpgsql STRICT SECURITY DEFINER
    AS $$
  declare
    xentity_id uuid;
    xversion_id uuid;
    xcard_version sg_public.card_version;
  begin
    xentity_id := uuid_generate_v4();
    xversion_id := uuid_generate_v4();
    insert into sg_public.entity
    (entity_id, entity_kind) values (xentity_id, 'card');
    insert into sg_public.card_entity
    (entity_id) values (xentity_id);
    insert into sg_public.entity_version
    (version_id, entity_kind) values (xversion_id, 'card');
    insert into sg_public.card_version
    (version_id, entity_id, language, name, tags, subject_id, kind, data)
    values (xversion_id, xentity_id, language, name, tags, subject_id, kind, data)
    returning * into xcard_version;
    return xcard_version;
  end;
$$;


--
-- Name: FUNCTION new_card(language character varying, name text, tags text[], subject_id uuid, kind sg_public.card_kind, data jsonb); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public.new_card(language character varying, name text, tags text[], subject_id uuid, kind sg_public.card_kind, data jsonb) IS 'Create a new card.';


--
-- Name: subject_version; Type: TABLE; Schema: sg_public; Owner: -
--

CREATE TABLE sg_public.subject_version (
    version_id uuid NOT NULL,
    created timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    modified timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    entity_id uuid NOT NULL,
    previous_version_id uuid,
    language character varying(5) DEFAULT 'en'::character varying NOT NULL,
    name text NOT NULL,
    status sg_public.entity_status DEFAULT 'pending'::sg_public.entity_status NOT NULL,
    available boolean DEFAULT true NOT NULL,
    tags text[] DEFAULT ARRAY[]::text[],
    user_id uuid,
    session_id uuid,
    body text NOT NULL,
    CONSTRAINT lang_check CHECK (((language)::text ~* '^\w{2}(-\w{2})?$'::text)),
    CONSTRAINT user_or_session CHECK (((user_id IS NOT NULL) OR (session_id IS NOT NULL)))
);


--
-- Name: TABLE subject_version; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TABLE sg_public.subject_version IS 'Every version of the subjects. A subject is a collection of cards and other subjects. A subject has many cards and other subjects.';


--
-- Name: COLUMN subject_version.version_id; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.subject_version.version_id IS 'The version ID -- a single subject can have many versions.';


--
-- Name: COLUMN subject_version.created; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.subject_version.created IS 'When a user created this version.';


--
-- Name: COLUMN subject_version.modified; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.subject_version.modified IS 'When a user last modified this version.';


--
-- Name: COLUMN subject_version.entity_id; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.subject_version.entity_id IS 'The overall entity ID.';


--
-- Name: COLUMN subject_version.previous_version_id; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.subject_version.previous_version_id IS 'The previous version this version is based on.';


--
-- Name: COLUMN subject_version.language; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.subject_version.language IS 'Which human language this subject contains.';


--
-- Name: COLUMN subject_version.name; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.subject_version.name IS 'The name of the subject.';


--
-- Name: COLUMN subject_version.status; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.subject_version.status IS 'The status of the subject. The latest accepted version is current.';


--
-- Name: COLUMN subject_version.available; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.subject_version.available IS 'Whether the subject is available to learners.';


--
-- Name: COLUMN subject_version.tags; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.subject_version.tags IS 'A list of tags. Think Bloom taxonomy.';


--
-- Name: COLUMN subject_version.user_id; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.subject_version.user_id IS 'Which user created this version.';


--
-- Name: COLUMN subject_version.session_id; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.subject_version.session_id IS 'If no user, which session created this version.';


--
-- Name: COLUMN subject_version.body; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.subject_version.body IS 'The description of the goals of the subject.';


--
-- Name: CONSTRAINT lang_check ON subject_version; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON CONSTRAINT lang_check ON sg_public.subject_version IS 'Languages must be BCP47 compliant.';


--
-- Name: CONSTRAINT user_or_session ON subject_version; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON CONSTRAINT user_or_session ON sg_public.subject_version IS 'Ensure only the user or session has data.';


--
-- Name: new_subject(character varying, text, text[], text, uuid[], uuid[]); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.new_subject(language character varying, name text, tags text[], body text, parent uuid[], before uuid[]) RETURNS sg_public.subject_version
    LANGUAGE plpgsql STRICT SECURITY DEFINER
    AS $$
  declare
    xentity_id uuid;
    xversion_id uuid;
    xsubject_version sg_public.subject_version;
  begin
    xentity_id := uuid_generate_v4();
    xversion_id := uuid_generate_v4();
    insert into sg_public.entity
    (entity_id, entity_kind) values (xentity_id, 'subject');
    insert into sg_public.subject_entity
    (entity_id) values (xentity_id);
    insert into sg_public.entity_version
    (version_id, entity_kind) values (xversion_id, 'subject');
    insert into sg_public.subject_version
    (version_id, entity_id, language, name, tags, body)
    values (xversion_id, xentity_id, language, name, tags, body)
    returning * into xsubject_version;
    insert into sg_public.subject_version_parent_child
    (child_version_id, parent_entity_id)
    select xversion_id, unnest(parent);
    insert into sg_public.subject_version_before_after
    (after_version_id, before_entity_id)
    select xversion_id, unnest(before);
    return xsubject_version;
  end;
$$;


--
-- Name: FUNCTION new_subject(language character varying, name text, tags text[], body text, parent uuid[], before uuid[]); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public.new_subject(language character varying, name text, tags text[], body text, parent uuid[], before uuid[]) IS 'Create a new subject.';


--
-- Name: subject; Type: VIEW; Schema: sg_public; Owner: -
--

CREATE VIEW sg_public.subject AS
 SELECT DISTINCT ON (subject_version.entity_id) subject_version.version_id,
    subject_version.created,
    subject_version.modified,
    subject_version.entity_id,
    subject_version.previous_version_id,
    subject_version.language,
    subject_version.name,
    subject_version.status,
    subject_version.available,
    subject_version.tags,
    subject_version.user_id,
    subject_version.session_id,
    subject_version.body
   FROM sg_public.subject_version
  WHERE (subject_version.status = 'accepted'::sg_public.entity_status)
  ORDER BY subject_version.entity_id, subject_version.created DESC;


--
-- Name: VIEW subject; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON VIEW sg_public.subject IS 'The latest accepted version of each subject.';


--
-- Name: search_subjects(text); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.search_subjects(query text) RETURNS SETOF sg_public.subject
    LANGUAGE sql STABLE
    AS $$
  with documents as (
    select
      entity_id,
      to_tsvector('english', unaccent(name)) ||
      to_tsvector('english', unaccent(array_to_string(tags, ' '))) ||
      to_tsvector('english', unaccent(body)) as document
    from sg_public.subject
  ),
  ranking as (
    select
      s.entity_id as entity_id,
      ts_rank(d.document, websearch_to_tsquery('english', unaccent(query))) as rank
    from
      sg_public.subject s,
      documents d
    where
      d.document @@ websearch_to_tsquery('english', unaccent(query))
      and s.entity_id = d.entity_id
    order by rank desc
  )
  select s.*
  from
    ranking r,
    sg_public.subject s
  where
    s.entity_id = r.entity_id
  order by r.rank desc;
$$;


--
-- Name: FUNCTION search_subjects(query text); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public.search_subjects(query text) IS 'Search subjects.';


--
-- Name: select_popular_subjects(); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.select_popular_subjects() RETURNS SETOF sg_public.subject
    LANGUAGE sql STABLE
    AS $$
  select *
  from sg_public.subject
  order by (
    select count(*)
    from sg_public.user_subject
    where subject_id = entity_id
  )
  limit 5;
$$;


--
-- Name: FUNCTION select_popular_subjects(); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public.select_popular_subjects() IS 'Select the 5 most popular subjects.';


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
    where sg_private.user.email = trim($1)
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
    where sg_private.user.email = trim($1)
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
  if (char_length(trim(password)) < 8) then
    raise exception 'I need at least 8 characters for passwords.'
      using errcode = '355CAC69';
  end if;
  insert into sg_public.user ("name")
    values (name)
    returning * into public_user;
  insert into sg_private.user ("user_id", "email", "password")
    values (public_user.id, email, crypt(trim(password), gen_salt('bf', 8)))
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
    set password = crypt(trim(new_password), gen_salt('bf', 8))
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
-- Name: card_entity; Type: TABLE; Schema: sg_public; Owner: -
--

CREATE TABLE sg_public.card_entity (
    entity_id uuid NOT NULL
);


--
-- Name: TABLE card_entity; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TABLE sg_public.card_entity IS 'A list of all card entity IDs';


--
-- Name: COLUMN card_entity.entity_id; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.card_entity.entity_id IS 'The ID of the entity';


--
-- Name: entity; Type: TABLE; Schema: sg_public; Owner: -
--

CREATE TABLE sg_public.entity (
    entity_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    entity_kind sg_public.entity_kind NOT NULL
);


--
-- Name: TABLE entity; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TABLE sg_public.entity IS 'A list of all entity IDs and their kinds.';


--
-- Name: COLUMN entity.entity_id; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.entity.entity_id IS 'The overall ID of the entity.';


--
-- Name: COLUMN entity.entity_kind; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.entity.entity_kind IS 'The kind of entity the ID represents.';


--
-- Name: entity_version; Type: TABLE; Schema: sg_public; Owner: -
--

CREATE TABLE sg_public.entity_version (
    version_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    entity_kind sg_public.entity_kind NOT NULL
);


--
-- Name: TABLE entity_version; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TABLE sg_public.entity_version IS 'A list of all entity version IDs and their kinds.';


--
-- Name: COLUMN entity_version.version_id; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.entity_version.version_id IS 'The ID of the version.';


--
-- Name: COLUMN entity_version.entity_kind; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.entity_version.entity_kind IS 'The kind of entity the ID represents.';


--
-- Name: subject_entity; Type: TABLE; Schema: sg_public; Owner: -
--

CREATE TABLE sg_public.subject_entity (
    entity_id uuid NOT NULL
);


--
-- Name: TABLE subject_entity; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TABLE sg_public.subject_entity IS 'A list of all subject entity IDs.';


--
-- Name: COLUMN subject_entity.entity_id; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.subject_entity.entity_id IS 'The ID of the entity.';


--
-- Name: subject_version_before_after; Type: TABLE; Schema: sg_public; Owner: -
--

CREATE TABLE sg_public.subject_version_before_after (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    created timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    modified timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    after_version_id uuid NOT NULL,
    before_entity_id uuid NOT NULL
);


--
-- Name: TABLE subject_version_before_after; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TABLE sg_public.subject_version_before_after IS 'A join table between a subject version and the subjects before.';


--
-- Name: COLUMN subject_version_before_after.id; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.subject_version_before_after.id IS 'The relationship ID.';


--
-- Name: COLUMN subject_version_before_after.created; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.subject_version_before_after.created IS 'When a user created this version.';


--
-- Name: COLUMN subject_version_before_after.modified; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.subject_version_before_after.modified IS 'When a user last modified this version.';


--
-- Name: COLUMN subject_version_before_after.after_version_id; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.subject_version_before_after.after_version_id IS 'The version ID of the after subject.';


--
-- Name: COLUMN subject_version_before_after.before_entity_id; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.subject_version_before_after.before_entity_id IS 'The entity ID of the before subject.';


--
-- Name: subject_version_parent_child; Type: TABLE; Schema: sg_public; Owner: -
--

CREATE TABLE sg_public.subject_version_parent_child (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    created timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    modified timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    child_version_id uuid NOT NULL,
    parent_entity_id uuid NOT NULL
);


--
-- Name: TABLE subject_version_parent_child; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TABLE sg_public.subject_version_parent_child IS 'A join table between a subject version and the parents.';


--
-- Name: COLUMN subject_version_parent_child.id; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.subject_version_parent_child.id IS 'The relationship ID.';


--
-- Name: COLUMN subject_version_parent_child.created; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.subject_version_parent_child.created IS 'When a user created this version.';


--
-- Name: COLUMN subject_version_parent_child.modified; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.subject_version_parent_child.modified IS 'When a user last modified this version.';


--
-- Name: COLUMN subject_version_parent_child.child_version_id; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.subject_version_parent_child.child_version_id IS 'The version ID of the child subject.';


--
-- Name: COLUMN subject_version_parent_child.parent_entity_id; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.subject_version_parent_child.parent_entity_id IS 'The entity ID of the parent subject.';


--
-- Name: user_subject; Type: TABLE; Schema: sg_public; Owner: -
--

CREATE TABLE sg_public.user_subject (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    created timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    modified timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    user_id uuid,
    session_id uuid,
    subject_id uuid NOT NULL,
    CONSTRAINT user_or_session CHECK (((user_id IS NOT NULL) OR (session_id IS NOT NULL)))
);


--
-- Name: TABLE user_subject; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TABLE sg_public.user_subject IS 'The association between a user and a subject. This is a subject the learner is learning.';


--
-- Name: COLUMN user_subject.id; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.user_subject.id IS 'The ID of the user subject.';


--
-- Name: COLUMN user_subject.created; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.user_subject.created IS 'When the user created the association.';


--
-- Name: COLUMN user_subject.modified; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.user_subject.modified IS 'When the association last changed.';


--
-- Name: COLUMN user_subject.user_id; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.user_subject.user_id IS 'Which user the association belongs to.';


--
-- Name: COLUMN user_subject.session_id; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.user_subject.session_id IS 'If not user, the session the association belongs to.';


--
-- Name: COLUMN user_subject.subject_id; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.user_subject.subject_id IS 'Which subject the association belongs to.';


--
-- Name: CONSTRAINT user_or_session ON user_subject; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON CONSTRAINT user_or_session ON sg_public.user_subject IS 'Ensure only the user or session has data.';


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
-- Name: card_entity card_entity_pkey; Type: CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.card_entity
    ADD CONSTRAINT card_entity_pkey PRIMARY KEY (entity_id);


--
-- Name: card_version card_version_pkey; Type: CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.card_version
    ADD CONSTRAINT card_version_pkey PRIMARY KEY (version_id);


--
-- Name: entity entity_entity_id_entity_kind_key; Type: CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.entity
    ADD CONSTRAINT entity_entity_id_entity_kind_key UNIQUE (entity_id, entity_kind);


--
-- Name: entity entity_pkey; Type: CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.entity
    ADD CONSTRAINT entity_pkey PRIMARY KEY (entity_id);


--
-- Name: entity_version entity_version_pkey; Type: CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.entity_version
    ADD CONSTRAINT entity_version_pkey PRIMARY KEY (version_id);


--
-- Name: entity_version entity_version_version_id_entity_kind_key; Type: CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.entity_version
    ADD CONSTRAINT entity_version_version_id_entity_kind_key UNIQUE (version_id, entity_kind);


--
-- Name: subject_entity subject_entity_pkey; Type: CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.subject_entity
    ADD CONSTRAINT subject_entity_pkey PRIMARY KEY (entity_id);


--
-- Name: subject_version_before_after subject_version_before_after_after_version_id_before_entity_key; Type: CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.subject_version_before_after
    ADD CONSTRAINT subject_version_before_after_after_version_id_before_entity_key UNIQUE (after_version_id, before_entity_id);


--
-- Name: subject_version_before_after subject_version_before_after_pkey; Type: CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.subject_version_before_after
    ADD CONSTRAINT subject_version_before_after_pkey PRIMARY KEY (id);


--
-- Name: subject_version_parent_child subject_version_parent_child_child_version_id_parent_entity_key; Type: CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.subject_version_parent_child
    ADD CONSTRAINT subject_version_parent_child_child_version_id_parent_entity_key UNIQUE (child_version_id, parent_entity_id);


--
-- Name: subject_version_parent_child subject_version_parent_child_pkey; Type: CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.subject_version_parent_child
    ADD CONSTRAINT subject_version_parent_child_pkey PRIMARY KEY (id);


--
-- Name: subject_version subject_version_pkey; Type: CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.subject_version
    ADD CONSTRAINT subject_version_pkey PRIMARY KEY (version_id);


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
-- Name: user_subject user_subject_pkey; Type: CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.user_subject
    ADD CONSTRAINT user_subject_pkey PRIMARY KEY (id);


--
-- Name: user_subject user_subject_session_id_subject_id_key; Type: CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.user_subject
    ADD CONSTRAINT user_subject_session_id_subject_id_key UNIQUE (session_id, subject_id);


--
-- Name: user_subject user_subject_user_id_subject_id_key; Type: CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.user_subject
    ADD CONSTRAINT user_subject_user_id_subject_id_key UNIQUE (user_id, subject_id);


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
-- Name: card_version insert_card_version_user_or_session; Type: TRIGGER; Schema: sg_public; Owner: -
--

CREATE TRIGGER insert_card_version_user_or_session BEFORE INSERT ON sg_public.card_version FOR EACH ROW EXECUTE PROCEDURE sg_private.insert_user_or_session();


--
-- Name: TRIGGER insert_card_version_user_or_session ON card_version; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TRIGGER insert_card_version_user_or_session ON sg_public.card_version IS 'Automatically add the user_id or session_id.';


--
-- Name: subject_version insert_subject_version_user_or_session; Type: TRIGGER; Schema: sg_public; Owner: -
--

CREATE TRIGGER insert_subject_version_user_or_session BEFORE INSERT ON sg_public.subject_version FOR EACH ROW EXECUTE PROCEDURE sg_private.insert_user_or_session();


--
-- Name: TRIGGER insert_subject_version_user_or_session ON subject_version; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TRIGGER insert_subject_version_user_or_session ON sg_public.subject_version IS 'Automatically add the user_id or session_id.';


--
-- Name: user_subject insert_user_subject_user_or_session; Type: TRIGGER; Schema: sg_public; Owner: -
--

CREATE TRIGGER insert_user_subject_user_or_session BEFORE INSERT ON sg_public.user_subject FOR EACH ROW EXECUTE PROCEDURE sg_private.insert_user_or_session();


--
-- Name: TRIGGER insert_user_subject_user_or_session ON user_subject; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TRIGGER insert_user_subject_user_or_session ON sg_public.user_subject IS 'Whenever I make a new user subject, auto fill the `user_id` column';


--
-- Name: user trim_user_name; Type: TRIGGER; Schema: sg_public; Owner: -
--

CREATE TRIGGER trim_user_name BEFORE INSERT ON sg_public."user" FOR EACH ROW EXECUTE PROCEDURE sg_private.trim_user_name();


--
-- Name: TRIGGER trim_user_name ON "user"; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TRIGGER trim_user_name ON sg_public."user" IS 'Trim the user''s name.';


--
-- Name: card_version update_card_version_modified; Type: TRIGGER; Schema: sg_public; Owner: -
--

CREATE TRIGGER update_card_version_modified BEFORE UPDATE ON sg_public.card_version FOR EACH ROW EXECUTE PROCEDURE sg_private.update_modified_column();


--
-- Name: TRIGGER update_card_version_modified ON card_version; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TRIGGER update_card_version_modified ON sg_public.card_version IS 'Whenever a card version changes, update the `modified` column.';


--
-- Name: subject_version_before_after update_subject_version_before_after_modified; Type: TRIGGER; Schema: sg_public; Owner: -
--

CREATE TRIGGER update_subject_version_before_after_modified BEFORE UPDATE ON sg_public.subject_version_before_after FOR EACH ROW EXECUTE PROCEDURE sg_private.update_modified_column();


--
-- Name: TRIGGER update_subject_version_before_after_modified ON subject_version_before_after; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TRIGGER update_subject_version_before_after_modified ON sg_public.subject_version_before_after IS 'Whenever a subject version changes, update the `modified` column.';


--
-- Name: subject_version update_subject_version_modified; Type: TRIGGER; Schema: sg_public; Owner: -
--

CREATE TRIGGER update_subject_version_modified BEFORE UPDATE ON sg_public.subject_version FOR EACH ROW EXECUTE PROCEDURE sg_private.update_modified_column();


--
-- Name: TRIGGER update_subject_version_modified ON subject_version; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TRIGGER update_subject_version_modified ON sg_public.subject_version IS 'Whenever a subject version changes, update the `modified` column.';


--
-- Name: subject_version_parent_child update_subject_version_parent_child_modified; Type: TRIGGER; Schema: sg_public; Owner: -
--

CREATE TRIGGER update_subject_version_parent_child_modified BEFORE UPDATE ON sg_public.subject_version_parent_child FOR EACH ROW EXECUTE PROCEDURE sg_private.update_modified_column();


--
-- Name: TRIGGER update_subject_version_parent_child_modified ON subject_version_parent_child; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TRIGGER update_subject_version_parent_child_modified ON sg_public.subject_version_parent_child IS 'Whenever a subject version changes, update the `modified` column.';


--
-- Name: user update_user_modified; Type: TRIGGER; Schema: sg_public; Owner: -
--

CREATE TRIGGER update_user_modified BEFORE UPDATE ON sg_public."user" FOR EACH ROW EXECUTE PROCEDURE sg_private.update_modified_column();


--
-- Name: TRIGGER update_user_modified ON "user"; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TRIGGER update_user_modified ON sg_public."user" IS 'Whenever the user changes, update the `modified` column.';


--
-- Name: user_subject update_user_subject_modified; Type: TRIGGER; Schema: sg_public; Owner: -
--

CREATE TRIGGER update_user_subject_modified BEFORE UPDATE ON sg_public.user_subject FOR EACH ROW EXECUTE PROCEDURE sg_private.update_modified_column();


--
-- Name: TRIGGER update_user_subject_modified ON user_subject; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TRIGGER update_user_subject_modified ON sg_public.user_subject IS 'Whenever a user subject changes, update the `modified` column.';


--
-- Name: user user_user_id_fkey; Type: FK CONSTRAINT; Schema: sg_private; Owner: -
--

ALTER TABLE ONLY sg_private."user"
    ADD CONSTRAINT user_user_id_fkey FOREIGN KEY (user_id) REFERENCES sg_public."user"(id) ON DELETE CASCADE;


--
-- Name: card_entity card_entity_entity_id_fkey; Type: FK CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.card_entity
    ADD CONSTRAINT card_entity_entity_id_fkey FOREIGN KEY (entity_id) REFERENCES sg_public.entity(entity_id);


--
-- Name: card_version card_version_entity_id_fkey; Type: FK CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.card_version
    ADD CONSTRAINT card_version_entity_id_fkey FOREIGN KEY (entity_id) REFERENCES sg_public.card_entity(entity_id);


--
-- Name: card_version card_version_previous_id_fkey; Type: FK CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.card_version
    ADD CONSTRAINT card_version_previous_id_fkey FOREIGN KEY (previous_id) REFERENCES sg_public.card_version(version_id);


--
-- Name: card_version card_version_subject_id_fkey; Type: FK CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.card_version
    ADD CONSTRAINT card_version_subject_id_fkey FOREIGN KEY (subject_id) REFERENCES sg_public.subject_entity(entity_id);


--
-- Name: card_version card_version_user_id_fkey; Type: FK CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.card_version
    ADD CONSTRAINT card_version_user_id_fkey FOREIGN KEY (user_id) REFERENCES sg_public."user"(id);


--
-- Name: card_version card_version_version_id_fkey; Type: FK CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.card_version
    ADD CONSTRAINT card_version_version_id_fkey FOREIGN KEY (version_id) REFERENCES sg_public.entity_version(version_id);


--
-- Name: subject_entity subject_entity_entity_id_fkey; Type: FK CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.subject_entity
    ADD CONSTRAINT subject_entity_entity_id_fkey FOREIGN KEY (entity_id) REFERENCES sg_public.entity(entity_id);


--
-- Name: subject_version_before_after subject_version_before_after_after_version_id_fkey; Type: FK CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.subject_version_before_after
    ADD CONSTRAINT subject_version_before_after_after_version_id_fkey FOREIGN KEY (after_version_id) REFERENCES sg_public.subject_version(version_id);


--
-- Name: subject_version_before_after subject_version_before_after_before_entity_id_fkey; Type: FK CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.subject_version_before_after
    ADD CONSTRAINT subject_version_before_after_before_entity_id_fkey FOREIGN KEY (before_entity_id) REFERENCES sg_public.subject_entity(entity_id);


--
-- Name: subject_version subject_version_entity_id_fkey; Type: FK CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.subject_version
    ADD CONSTRAINT subject_version_entity_id_fkey FOREIGN KEY (entity_id) REFERENCES sg_public.subject_entity(entity_id);


--
-- Name: subject_version_parent_child subject_version_parent_child_child_version_id_fkey; Type: FK CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.subject_version_parent_child
    ADD CONSTRAINT subject_version_parent_child_child_version_id_fkey FOREIGN KEY (child_version_id) REFERENCES sg_public.subject_version(version_id);


--
-- Name: subject_version_parent_child subject_version_parent_child_parent_entity_id_fkey; Type: FK CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.subject_version_parent_child
    ADD CONSTRAINT subject_version_parent_child_parent_entity_id_fkey FOREIGN KEY (parent_entity_id) REFERENCES sg_public.subject_entity(entity_id);


--
-- Name: subject_version subject_version_previous_version_id_fkey; Type: FK CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.subject_version
    ADD CONSTRAINT subject_version_previous_version_id_fkey FOREIGN KEY (previous_version_id) REFERENCES sg_public.subject_version(version_id);


--
-- Name: subject_version subject_version_user_id_fkey; Type: FK CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.subject_version
    ADD CONSTRAINT subject_version_user_id_fkey FOREIGN KEY (user_id) REFERENCES sg_public."user"(id);


--
-- Name: subject_version subject_version_version_id_fkey; Type: FK CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.subject_version
    ADD CONSTRAINT subject_version_version_id_fkey FOREIGN KEY (version_id) REFERENCES sg_public.entity_version(version_id);


--
-- Name: user_subject user_subject_subject_id_fkey; Type: FK CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.user_subject
    ADD CONSTRAINT user_subject_subject_id_fkey FOREIGN KEY (subject_id) REFERENCES sg_public.subject_entity(entity_id);


--
-- Name: user_subject user_subject_user_id_fkey; Type: FK CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.user_subject
    ADD CONSTRAINT user_subject_user_id_fkey FOREIGN KEY (user_id) REFERENCES sg_public."user"(id) ON DELETE CASCADE;


--
-- Name: user delete_user; Type: POLICY; Schema: sg_public; Owner: -
--

CREATE POLICY delete_user ON sg_public."user" FOR DELETE TO sg_user USING ((id = (current_setting('jwt.claims.user_id'::text))::uuid));


--
-- Name: user delete_user_admin; Type: POLICY; Schema: sg_public; Owner: -
--

CREATE POLICY delete_user_admin ON sg_public."user" FOR DELETE TO sg_admin USING (true);


--
-- Name: user_subject delete_user_subject; Type: POLICY; Schema: sg_public; Owner: -
--

CREATE POLICY delete_user_subject ON sg_public.user_subject FOR DELETE TO sg_user, sg_admin USING ((user_id = (current_setting('jwt.claims.user_id'::text))::uuid));


--
-- Name: user_subject insert_user_subject; Type: POLICY; Schema: sg_public; Owner: -
--

CREATE POLICY insert_user_subject ON sg_public.user_subject FOR INSERT TO sg_user, sg_admin;


--
-- Name: user select_user; Type: POLICY; Schema: sg_public; Owner: -
--

CREATE POLICY select_user ON sg_public."user" FOR SELECT USING (true);


--
-- Name: user_subject select_user_subject; Type: POLICY; Schema: sg_public; Owner: -
--

CREATE POLICY select_user_subject ON sg_public.user_subject FOR SELECT TO sg_user, sg_admin USING ((user_id = (current_setting('jwt.claims.user_id'::text))::uuid));


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
-- Name: user_subject; Type: ROW SECURITY; Schema: sg_public; Owner: -
--

ALTER TABLE sg_public.user_subject ENABLE ROW LEVEL SECURITY;

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
    ('20190227220630'),
    ('20190319234401'),
    ('20190322230728');
