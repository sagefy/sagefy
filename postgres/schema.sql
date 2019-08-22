SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
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
-- Name: next_option; Type: TYPE; Schema: sg_public; Owner: -
--

CREATE TYPE sg_public.next_option AS ENUM (
    'complete_subject',
    'choose_step',
    'create_card',
    'learn_card'
);


--
-- Name: TYPE next_option; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TYPE sg_public.next_option IS 'List of next page options.';


--
-- Name: next_page; Type: TYPE; Schema: sg_public; Owner: -
--

CREATE TYPE sg_public.next_page AS (
	goal uuid,
	step uuid,
	next sg_public.next_option,
	kind sg_public.card_kind,
	card uuid
);


--
-- Name: TYPE next_page; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TYPE sg_public.next_page IS 'Describes the next page to go to in the experience.';


--
-- Name: post_kind; Type: TYPE; Schema: sg_public; Owner: -
--

CREATE TYPE sg_public.post_kind AS ENUM (
    'post',
    'proposal',
    'vote'
);


--
-- Name: TYPE post_kind; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TYPE sg_public.post_kind IS 'The three kinds of posts.';


--
-- Name: search_result; Type: TYPE; Schema: sg_public; Owner: -
--

CREATE TYPE sg_public.search_result AS (
	entity_id uuid,
	kind text,
	subkind text,
	name text,
	body jsonb
);


--
-- Name: TYPE search_result; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TYPE sg_public.search_result IS 'The format of a search result entry.';


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
-- Name: slugify(text); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.slugify(value text) RETURNS text
    LANGUAGE sql IMMUTABLE STRICT
    AS $_$
  -- from https://www.kdobson.net/2019/ultimate-postgresql-slug-function/
  -- removes accents (diacritic signs) from a given string --
  WITH "unaccented" AS (
    SELECT unaccent("value") AS "value"
  ),
  -- lowercases the string
  "lowercase" AS (
    SELECT lower("value") AS "value"
    FROM "unaccented"
  ),
  -- remove single and double quotes
  "removed_quotes" AS (
    SELECT regexp_replace("value", '[''"]+', '', 'gi') AS "value"
    FROM "lowercase"
  ),
  -- replaces anything that's not a letter, number, hyphen('-'), or underscore('_') with a hyphen('-')
  "hyphenated" AS (
    SELECT regexp_replace("value", '[^a-z0-9\\-_]+', '-', 'gi') AS "value"
    FROM "removed_quotes"
  ),
  -- trims hyphens('-') if they exist on the head or tail of the string
  "trimmed" AS (
    SELECT regexp_replace(regexp_replace("value", '\-+$', ''), '^\-', '') AS "value"
    FROM "hyphenated"
  )
  SELECT "value" FROM "trimmed";
$_$;


--
-- Name: FUNCTION slugify(value text); Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON FUNCTION public.slugify(value text) IS 'Given a string, turn it into a URL slug.';


--
-- Name: text_array_to_text(text[]); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.text_array_to_text(arr text[]) RETURNS text
    LANGUAGE sql IMMUTABLE
    AS $$
  select array_to_string(arr, ' ');
$$;


--
-- Name: FUNCTION text_array_to_text(arr text[]); Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON FUNCTION public.text_array_to_text(arr text[]) IS 'Convert an array of text to a single text.';


--
-- Name: text_concat_ws(text, text[]); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.text_concat_ws(text, VARIADIC text[]) RETURNS text
    LANGUAGE internal IMMUTABLE
    AS $$text_concat_ws$$;


--
-- Name: FUNCTION text_concat_ws(text, VARIADIC text[]); Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON FUNCTION public.text_concat_ws(text, VARIADIC text[]) IS 'Concat a list of plain text to a single text.';


--
-- Name: insert_card_version_status(); Type: FUNCTION; Schema: sg_private; Owner: -
--

CREATE FUNCTION sg_private.insert_card_version_status() RETURNS trigger
    LANGUAGE plpgsql STRICT SECURITY DEFINER
    AS $$
begin
  new.status = 'accepted'::sg_public.entity_status;
  return new;
end;
$$;


--
-- Name: FUNCTION insert_card_version_status(); Type: COMMENT; Schema: sg_private; Owner: -
--

COMMENT ON FUNCTION sg_private.insert_card_version_status() IS 'When inserting a new card, automatically set the status to accepted.';


--
-- Name: insert_subject_version_status(); Type: FUNCTION; Schema: sg_private; Owner: -
--

CREATE FUNCTION sg_private.insert_subject_version_status() RETURNS trigger
    LANGUAGE plpgsql STRICT SECURITY DEFINER
    AS $$
begin
  new.status = 'accepted'::sg_public.entity_status;
  return new;
end;
$$;


--
-- Name: FUNCTION insert_subject_version_status(); Type: COMMENT; Schema: sg_private; Owner: -
--

COMMENT ON FUNCTION sg_private.insert_subject_version_status() IS 'When inserting a new subject, automatically set the status to accepted.';


--
-- Name: insert_user_or_session(); Type: FUNCTION; Schema: sg_private; Owner: -
--

CREATE FUNCTION sg_private.insert_user_or_session() RETURNS trigger
    LANGUAGE plpgsql STRICT SECURITY DEFINER
    AS $$
declare
  xuser_id uuid;
  xsession_id uuid;
begin
  xuser_id := nullif(current_setting('jwt.claims.user_id', true), '')::uuid;
  xsession_id := nullif(current_setting('jwt.claims.session_id', true), '')::uuid;
  if (xuser_id is not null) then
    new.user_id = xuser_id;
  elsif (xsession_id is not null) then
    new.session_id = xsession_id;
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
-- Name: score_response(); Type: FUNCTION; Schema: sg_private; Owner: -
--

CREATE FUNCTION sg_private.score_response() RETURNS trigger
    LANGUAGE plpgsql STRICT SECURITY DEFINER
    AS $$
  declare
    card sg_public.card;
    subject sg_public.subject;
    prior sg_public.response;
    prior_learned real;
    option jsonb;
    score real;
    learned real;
    slip constant real := 0.1;
    guess constant real := 0.3;
    transit constant real := 0.05;
  begin
    -- Overall: Fill in (subject_id, score, learned)
    -- Validate if the response to the card is valid.
    select c.* into card
    from sg_public.card c
    where c.entity_id = new.card_id
    limit 1;
    if (card.kind is null) then
      raise exception 'No card found.' using errcode = 'EE05C989';
    end if;
    if (card.kind <> 'choice') then -- scored kinds only
      raise exception 'You may only respond to a scored card.'
        using errcode = '1306BF1C';
    end if;
    option := card.data->'options'->new.response;
    if (option is null) then
      raise exception 'You must submit an available response `id`.'
        using errcode = '681942FD';
    end if;
    -- Set default values
    new.subject_id := card.subject_id;
    -- Score the response
    new.score := (option->>'correct')::boolean::int::real;
    -- Calculate p(learned)
    select s.* into subject
    from sg_public.subject s
    where entity_id = card.subject_id;
    prior_learned := (select sg_public.subject_learned(subject));
    learned := (
      new.score * (
        (prior_learned * (1 - slip)) /
        (prior_learned * (1 - slip) + (1 - prior_learned) * guess)
      ) +
      (1 - new.score) * (
        (prior_learned * slip) /
        (prior_learned * slip + (1 - prior_learned) * (1 - guess))
      )
    );
    new.learned := learned + (1 - learned) * transit;
    return new;
  end;
$$;


--
-- Name: FUNCTION score_response(); Type: COMMENT; Schema: sg_private; Owner: -
--

COMMENT ON FUNCTION sg_private.score_response() IS 'After I respond to a card, score the result and update model.';


--
-- Name: subject_auto_user_subject(); Type: FUNCTION; Schema: sg_private; Owner: -
--

CREATE FUNCTION sg_private.subject_auto_user_subject() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin
  insert into sg_public.user_subject (subject_id)
  values (new.entity_id)
  on conflict do nothing;
  return new;
end;
$$;


--
-- Name: FUNCTION subject_auto_user_subject(); Type: COMMENT; Schema: sg_private; Owner: -
--

COMMENT ON FUNCTION sg_private.subject_auto_user_subject() IS 'Whenever I make a new subject version, add me as a learner.';


--
-- Name: subject_unique_name(); Type: FUNCTION; Schema: sg_private; Owner: -
--

CREATE FUNCTION sg_private.subject_unique_name() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
declare
  xprev sg_public.subject_version;
begin
  select s.* into xprev
  from sg_public.subject s
  where slugify(s.name) = slugify(new.name)
  and s.entity_id <> new.entity_id;
  if (found) then
    raise exception 'Subject name in use.' using errcode = '5E310F2E';
  end if;
  return new;
end;
$$;


--
-- Name: FUNCTION subject_unique_name(); Type: COMMENT; Schema: sg_private; Owner: -
--

COMMENT ON FUNCTION sg_private.subject_unique_name() IS 'Ensure new subject versions have a unique name.';


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
-- Name: verify_post(); Type: FUNCTION; Schema: sg_private; Owner: -
--

CREATE FUNCTION sg_private.verify_post() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
  declare
    parent sg_public.post;
  begin
    if (new.parent_id) then
      select * into parent
      from sg_public.post
      where id = new.parent_id;
      if (parent.topic_id <> new.topic_id) then
        raise exception 'A reply must belong to the same topic.'
          using errcode = '76177573';
      end if;
      if (new.kind = 'vote' and parent.kind <> 'proposal') then
        raise exception 'A vote may only reply to a proposal.'
          using errcode = '8DF72C56';
      end if;
      if (new.kind = 'vote' and parent.user_id = new.user_id) then
        raise exception 'A user cannot vote on their own proposal.'
          using errcode = 'E47E0411';
      end if;
    end if;
    return new;
  end;
$$;


--
-- Name: FUNCTION verify_post(); Type: COMMENT; Schema: sg_private; Owner: -
--

COMMENT ON FUNCTION sg_private.verify_post() IS 'Verify valid data when creating or updating a post.';


--
-- Name: anonymous_token(); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.anonymous_token() RETURNS sg_public.jwt_token
    LANGUAGE sql
    AS $$
  select ('sg_anonymous', null, uuid_generate_v4(), null)::sg_public.jwt_token;
$$;


--
-- Name: FUNCTION anonymous_token(); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public.anonymous_token() IS 'Create anonymous user token.';


SET default_tablespace = '';

SET default_with_oids = false;

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
-- Name: card; Type: VIEW; Schema: sg_public; Owner: -
--

CREATE VIEW sg_public.card AS
 SELECT DISTINCT ON (card_version.entity_id) card_version.version_id,
    card_version.created,
    card_version.modified,
    card_version.entity_id,
    card_version.previous_id,
    card_version.language,
    card_version.name,
    card_version.status,
    card_version.available,
    card_version.tags,
    card_version.user_id,
    card_version.session_id,
    card_version.subject_id,
    card_version.kind,
    card_version.data
   FROM sg_public.card_version
  WHERE (card_version.status = 'accepted'::sg_public.entity_status)
  ORDER BY card_version.entity_id, card_version.created DESC;


--
-- Name: VIEW card; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON VIEW sg_public.card IS 'The latest accepted version of each card.';


--
-- Name: card_by_entity_id(uuid); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.card_by_entity_id(entity_id uuid) RETURNS sg_public.card
    LANGUAGE sql STABLE
    AS $_$
  select c.*
  from sg_public.card c
  where c.entity_id = $1
  limit 1;
$_$;


--
-- Name: FUNCTION card_by_entity_id(entity_id uuid); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public.card_by_entity_id(entity_id uuid) IS 'Get the latest version of the card.';


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
    details text,
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
-- Name: COLUMN subject_version.details; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.subject_version.details IS 'The details of the subject.';


--
-- Name: CONSTRAINT lang_check ON subject_version; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON CONSTRAINT lang_check ON sg_public.subject_version IS 'Languages must be BCP47 compliant.';


--
-- Name: CONSTRAINT user_or_session ON subject_version; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON CONSTRAINT user_or_session ON sg_public.subject_version IS 'Ensure only the user or session has data.';


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
    subject_version.body,
    subject_version.details
   FROM sg_public.subject_version
  WHERE (subject_version.status = 'accepted'::sg_public.entity_status)
  ORDER BY subject_version.entity_id, subject_version.created DESC;


--
-- Name: VIEW subject; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON VIEW sg_public.subject IS 'The latest accepted version of each subject.';


--
-- Name: card_subject(sg_public.card); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.card_subject(card sg_public.card) RETURNS sg_public.subject
    LANGUAGE sql STABLE
    AS $_$
  select s.*
  from sg_public.subject s
  where s.entity_id = $1.subject_id;
$_$;


--
-- Name: FUNCTION card_subject(card sg_public.card); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public.card_subject(card sg_public.card) IS 'Get the card''s subject.';


--
-- Name: cards_by_current_user(); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.cards_by_current_user() RETURNS SETOF sg_public.card
    LANGUAGE sql STABLE
    AS $$
  select *
  from sg_public.card
  where entity_id in (
    select entity_id
    from sg_public.card_version
    where user_id = nullif(current_setting('jwt.claims.user_id', true), '')::uuid
  );
$$;


--
-- Name: FUNCTION cards_by_current_user(); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public.cards_by_current_user() IS 'Select cards I created or worked on.';


--
-- Name: choose_card(uuid); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.choose_card(subject_id uuid) RETURNS sg_public.card
    LANGUAGE plpgsql
    AS $_$
  declare
    xsubject sg_public.subject;
    xprior sg_public.response;
    kinds sg_public.card_kind[];
    xcard sg_public.card;
  begin
    select * into xsubject
    from sg_public.subject
    where entity_id = $1;
    select * into xprior
    from sg_public.subject_latest_response(xsubject);
    if (random() < (0.5 + 0.5 * sg_public.subject_learned(xsubject))) then
      kinds := array['choice'];
    else
      kinds := array['video', 'page', 'unscored_embed'];
    end if;
    select c.* into xcard
    from sg_public.card c
    where c.subject_id = $1
      and c.kind = any(kinds)
      and (xprior.card_id is null or c.entity_id <> xprior.card_id)
      and random() < sg_public.subject_card_count(xsubject) / 10::real
    order by random()
    limit 1;
    return xcard;
  end;
  -- Future version: When estimating parameters and the card kind is scored,
  -- prefer 0.25 < correct < 0.75
$_$;


--
-- Name: FUNCTION choose_card(subject_id uuid); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public.choose_card(subject_id uuid) IS 'After I select a subject, search for a suitable card.';


--
-- Name: create_card(character varying, text, text[], uuid, sg_public.card_kind, jsonb); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.create_card(language character varying, name text, tags text[], subject_id uuid, kind sg_public.card_kind, data jsonb) RETURNS sg_public.card_version
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
-- Name: FUNCTION create_card(language character varying, name text, tags text[], subject_id uuid, kind sg_public.card_kind, data jsonb); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public.create_card(language character varying, name text, tags text[], subject_id uuid, kind sg_public.card_kind, data jsonb) IS 'Create a new card.';


--
-- Name: create_email_token(text); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.create_email_token(email text) RETURNS void
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
-- Name: FUNCTION create_email_token(email text); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public.create_email_token(email text) IS 'Generate and email a token to update email.';


--
-- Name: create_password_token(text); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.create_password_token(email text) RETURNS void
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
-- Name: FUNCTION create_password_token(email text); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public.create_password_token(email text) IS 'Generate and email a token to update password.';


--
-- Name: create_subject(character varying, text, text[], text, uuid[], uuid[]); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.create_subject(language character varying, name text, tags text[], body text, parent uuid[], before uuid[]) RETURNS sg_public.subject_version
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
-- Name: FUNCTION create_subject(language character varying, name text, tags text[], body text, parent uuid[], before uuid[]); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public.create_subject(language character varying, name text, tags text[], body text, parent uuid[], before uuid[]) IS 'Create a new subject.';


--
-- Name: create_user(text, text, text); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.create_user(name text, email text, password text) RETURNS sg_public.jwt_token
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
-- Name: current_user(); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public."current_user"() RETURNS sg_public."user"
    LANGUAGE sql STABLE
    AS $$
  select *
  from sg_public.user
  where id = nullif(current_setting('jwt.claims.user_id', true), '')::uuid
$$;


--
-- Name: FUNCTION "current_user"(); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public."current_user"() IS 'Get the current logged in user.';


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
-- Name: next(uuid, uuid); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.next(goal_entity_id uuid, step_entity_id uuid DEFAULT NULL::uuid) RETURNS sg_public.next_page
    LANGUAGE plpgsql
    AS $$
  declare
    xgoal sg_public.subject;
    xstep sg_public.subject;
    xcard sg_public.card;
    xnext uuid[];
  begin
    -- First we'll validate the goal by selecting it
    select s.* into xgoal
    from sg_public.subject s
    where s.entity_id = goal_entity_id;
    -- Select the step if it exists
    select s.* into xstep
    from sg_public.subject s
    where s.entity_id = step_entity_id;
    -- Always attempt to add the goal to user_subject
    insert into sg_public.user_subject (subject_id)
    values (xgoal.entity_id)
    on conflict do nothing;
    -- If there's no step, or p(learned >= 0.99)..
    -- -- Nota bene: `row(...) is not null` behaves unexpectedly! Beware!
    if (xstep is null or sg_public.subject_learned(xstep) >= 0.99) then
      -- We need to choose the next step...
      xnext := array(
        select entity_id
        from sg_public.subject_next_child_subjects(xgoal)
      );
      -- If there's no next step, then we are done
      if (array_length(xnext, 1) is null) then
        return (
          xgoal.entity_id,
          null,
          'complete_subject'::sg_public.next_option,
          null,
          null
        )::sg_public.next_page;
      end if;
      -- If there's exactly one step level, choose it automatically
      if (array_length(xnext, 1) = 1) then
        return sg_public.next(xgoal.entity_id, xnext[1]);
      end if;
      -- Otherwise, let the learner choose the next step
      return (
        xgoal.entity_id,
        null,
        'choose_step'::sg_public.next_option,
        null,
        null
      )::sg_public.next_page;
    end if;
    -- If there's a step, and p(learned) < 0.99...
    select * into xcard
    from sg_public.choose_card(xstep.entity_id);
    -- Create a card if there isn't one
    if (xcard is null) then
      return (
        xgoal.entity_id,
        xstep.entity_id,
        'create_card'::sg_public.next_option,
        null,
        null
      )::sg_public.next_page;
    end if;
    -- Learn a card
    return (
      xgoal.entity_id,
      xstep.entity_id,
      'learn_card'::sg_public.next_option,
      xcard.kind,
      xcard.entity_id
    )::sg_public.next_page;
  end;
$$;


--
-- Name: FUNCTION next(goal_entity_id uuid, step_entity_id uuid); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public.next(goal_entity_id uuid, step_entity_id uuid) IS 'Determine the next thing to do.';


--
-- Name: popular_subjects(); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.popular_subjects() RETURNS SETOF sg_public.subject
    LANGUAGE sql STABLE
    AS $$
  with most_popular as (
    select s.*
    from sg_public.subject s
    order by sg_public.subject_user_count(s) desc
    limit 20
  )
  select *
  from most_popular
  where name not ilike '%what is sagefy?%'
  order by random()
  limit 4;
$$;


--
-- Name: FUNCTION popular_subjects(); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public.popular_subjects() IS 'Select the 5 most popular subjects.';


--
-- Name: search_cards(text); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.search_cards(query text) RETURNS SETOF sg_public.card
    LANGUAGE sql STABLE
    AS $$
  -- If you see this in the future... NB the `to_tsvector` calls are indexed.
  -- if this part changes, you need to replace the index too.
  with r as (
    select
      distinct on (entity_id) entity_id,
      ts_rank(
        to_tsvector('english_unaccent', text_concat_ws(' ',
          name, text_array_to_text(tags), data::text
        )),
        websearch_to_tsquery('english_unaccent', query)
      ) as rank
    from sg_public.card_version
    where to_tsvector('english_unaccent', text_concat_ws(' ',
      name, text_array_to_text(tags), data::text
    )) @@ websearch_to_tsquery('english_unaccent', query)
    order by entity_id, rank
  )
  select c.*
  from sg_public.card c, r
  where c.entity_id = r.entity_id
  order by r.rank desc;
$$;


--
-- Name: FUNCTION search_cards(query text); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public.search_cards(query text) IS 'Search cards.';


--
-- Name: search_entities(text); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.search_entities(query text) RETURNS SETOF sg_public.search_result
    LANGUAGE sql STABLE
    AS $$
  select
    s.entity_id as entity_id,
    'subject' as kind,
    'subject' as subkind,
    s.name as name,
    to_jsonb(s.body) as body
  from sg_public.search_subjects(query) s
  union all
  select
    c.entity_id as entity_id,
    'card' as kind,
    c.kind::text as subkind,
    c.name as name,
    c.data as body
  from sg_public.search_cards(query) c;
$$;


--
-- Name: FUNCTION search_entities(query text); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public.search_entities(query text) IS 'Search subjects and cards.';


--
-- Name: search_subjects(text); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.search_subjects(query text) RETURNS SETOF sg_public.subject
    LANGUAGE sql STABLE
    AS $$
  -- If you see this in the future... NB the `to_tsvector` calls are indexed.
  -- if this part changes, you need to replace the index too.
  with r as (
    select
      distinct on (entity_id) entity_id,
      ts_rank(
        to_tsvector('english_unaccent', text_concat_ws(' ',
          name, text_array_to_text(tags), body
        )),
        websearch_to_tsquery('english_unaccent', query)
      ) as rank
    from sg_public.subject_version
    where to_tsvector('english_unaccent', text_concat_ws(' ',
      name, text_array_to_text(tags), body
    )) @@ websearch_to_tsquery('english_unaccent', query)
    order by entity_id, rank
  )
  select s.*
  from sg_public.subject s, r
  where s.entity_id = r.entity_id
  order by r.rank desc;
$$;


--
-- Name: FUNCTION search_subjects(query text); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public.search_subjects(query text) IS 'Search subjects.';


--
-- Name: subject_after_subjects(sg_public.subject); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.subject_after_subjects(subject sg_public.subject) RETURNS SETOF sg_public.subject
    LANGUAGE sql STABLE
    AS $_$
  select s.*
  from
    sg_public.subject s,
    sg_public.subject_version_before_after svba
  where
    svba.before_entity_id = $1.entity_id
    and s.version_id = svba.after_version_id;
$_$;


--
-- Name: FUNCTION subject_after_subjects(subject sg_public.subject); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public.subject_after_subjects(subject sg_public.subject) IS 'Get all the direct afters for a subject.';


--
-- Name: subject_all_after_count(sg_public.subject); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.subject_all_after_count(subject sg_public.subject) RETURNS bigint
    LANGUAGE sql STABLE
    AS $_$
  select count(*)
  from sg_public.subject_all_after_subjects($1);
$_$;


--
-- Name: FUNCTION subject_all_after_count(subject sg_public.subject); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public.subject_all_after_count(subject sg_public.subject) IS 'Count the number of subjects after the subject.';


--
-- Name: subject_all_after_subjects(sg_public.subject); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.subject_all_after_subjects(subject sg_public.subject) RETURNS SETOF sg_public.subject
    LANGUAGE sql STABLE
    AS $$
  with recursive all_afters as (
    select scs.*
    from sg_public.subject_after_subjects(subject) scs
    union all
    select scs.*
    from
      all_afters,
      lateral sg_public.subject_after_subjects(all_afters) scs
  )
  select *
  from all_afters;
$$;


--
-- Name: FUNCTION subject_all_after_subjects(subject sg_public.subject); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public.subject_all_after_subjects(subject sg_public.subject) IS 'Collects all the afters of the before subject.';


--
-- Name: subject_all_child_subjects(sg_public.subject); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.subject_all_child_subjects(subject sg_public.subject) RETURNS SETOF sg_public.subject
    LANGUAGE sql STABLE
    AS $$
  with recursive all_children as (
    select scs.*
    from sg_public.subject_child_subjects(subject) scs
    union all
    select scs.*
    from
      all_children,
      lateral sg_public.subject_child_subjects(all_children) scs
  )
  select *
  from all_children;
$$;


--
-- Name: FUNCTION subject_all_child_subjects(subject sg_public.subject); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public.subject_all_child_subjects(subject sg_public.subject) IS 'Collects all the children of the parent subject.';


--
-- Name: subject_before_subjects(sg_public.subject); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.subject_before_subjects(subject sg_public.subject) RETURNS SETOF sg_public.subject
    LANGUAGE sql STABLE
    AS $_$
  select s.*
  from
    sg_public.subject s,
    sg_public.subject_version_before_after svba
  where
    svba.after_version_id = $1.version_id
    and s.entity_id = svba.before_entity_id;
$_$;


--
-- Name: FUNCTION subject_before_subjects(subject sg_public.subject); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public.subject_before_subjects(subject sg_public.subject) IS 'Get all the direct befores for a subject.';


--
-- Name: subject_by_entity_id(uuid); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.subject_by_entity_id(entity_id uuid) RETURNS sg_public.subject
    LANGUAGE sql STABLE
    AS $_$
  select s.*
  from sg_public.subject s
  where s.entity_id = $1
  limit 1;
$_$;


--
-- Name: FUNCTION subject_by_entity_id(entity_id uuid); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public.subject_by_entity_id(entity_id uuid) IS 'Get a subject by entity id.';


--
-- Name: subject_card_count(sg_public.subject); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.subject_card_count(subject sg_public.subject) RETURNS bigint
    LANGUAGE sql STABLE
    AS $_$
  select count(c.*) from sg_public.subject_cards($1) c;
$_$;


--
-- Name: FUNCTION subject_card_count(subject sg_public.subject); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public.subject_card_count(subject sg_public.subject) IS 'Count the number of cards directly on the subject.';


--
-- Name: subject_cards(sg_public.subject); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.subject_cards(subject sg_public.subject) RETURNS SETOF sg_public.card
    LANGUAGE sql STABLE
    AS $_$
  select c.*
  from sg_public.card c
  where c.subject_id = $1.entity_id;
$_$;


--
-- Name: FUNCTION subject_cards(subject sg_public.subject); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public.subject_cards(subject sg_public.subject) IS 'List the number of cards directly on the subject.';


--
-- Name: subject_child_count(sg_public.subject); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.subject_child_count(subject sg_public.subject) RETURNS bigint
    LANGUAGE sql STABLE
    AS $$
  select count(*)
  from sg_public.subject_child_subjects(subject);
$$;


--
-- Name: FUNCTION subject_child_count(subject sg_public.subject); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public.subject_child_count(subject sg_public.subject) IS 'Count the number of children directly on the subject.';


--
-- Name: subject_child_subjects(sg_public.subject); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.subject_child_subjects(subject sg_public.subject) RETURNS SETOF sg_public.subject
    LANGUAGE sql STABLE
    AS $_$
  select s.*
  from
    sg_public.subject s,
    sg_public.subject_version_parent_child svpc
  where
    svpc.parent_entity_id = $1.entity_id
    and s.version_id = svpc.child_version_id;
$_$;


--
-- Name: FUNCTION subject_child_subjects(subject sg_public.subject); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public.subject_child_subjects(subject sg_public.subject) IS 'Collects the direct children of the parent subject.';


--
-- Name: subject_has_needed_before(sg_public.subject, uuid[]); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.subject_has_needed_before(sg_public.subject, uuid[]) RETURNS boolean
    LANGUAGE sql STABLE
    AS $_$
  select exists(
    select x.entity_id
    from sg_public.subject_before_subjects($1) x
    where sg_public.subject_learned(x) < 0.99
    and x.entity_id = any($2)
  );
$_$;


--
-- Name: FUNCTION subject_has_needed_before(sg_public.subject, uuid[]); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public.subject_has_needed_before(sg_public.subject, uuid[]) IS 'Does the learner/subject have a needed before?';


--
-- Name: response; Type: TABLE; Schema: sg_public; Owner: -
--

CREATE TABLE sg_public.response (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    created timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    modified timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    user_id uuid,
    session_id uuid,
    card_id uuid NOT NULL,
    subject_id uuid NOT NULL,
    response text NOT NULL,
    score real NOT NULL,
    learned real NOT NULL,
    CONSTRAINT response_score_check CHECK (((score >= (0)::double precision) AND (score <= (1)::double precision))),
    CONSTRAINT response_score_check1 CHECK (((score >= (0)::double precision) AND (score <= (1)::double precision))),
    CONSTRAINT user_or_session CHECK (((user_id IS NOT NULL) OR (session_id IS NOT NULL)))
);


--
-- Name: TABLE response; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TABLE sg_public.response IS 'When a learner responds to a card, we record the result.';


--
-- Name: COLUMN response.id; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.response.id IS 'The ID of the response.';


--
-- Name: COLUMN response.created; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.response.created IS 'When the user created the response.';


--
-- Name: COLUMN response.modified; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.response.modified IS 'When the system last modified the response.';


--
-- Name: COLUMN response.user_id; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.response.user_id IS 'The user the response belongs to.';


--
-- Name: COLUMN response.session_id; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.response.session_id IS 'If not user, the session_id the response belongs to.';


--
-- Name: COLUMN response.card_id; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.response.card_id IS 'The card (entity id) that the response belongs to.';


--
-- Name: COLUMN response.subject_id; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.response.subject_id IS 'The subject (entity id) that the response belongs to... at the time of the response';


--
-- Name: COLUMN response.response; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.response.response IS 'How the user responded.';


--
-- Name: COLUMN response.score; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.response.score IS 'The score, 0->1, of the response.';


--
-- Name: COLUMN response.learned; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.response.learned IS 'The estimated probability the learner has learned the subject, after this response.';


--
-- Name: CONSTRAINT user_or_session ON response; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON CONSTRAINT user_or_session ON sg_public.response IS 'Ensure only the user or session has data.';


--
-- Name: subject_latest_response(sg_public.subject); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.subject_latest_response(subject sg_public.subject) RETURNS sg_public.response
    LANGUAGE sql STABLE
    AS $_$
  select r.*
  from sg_public.response r
  where r.subject_id = $1.entity_id and (
    user_id = nullif(current_setting('jwt.claims.user_id', true), '')::uuid
    or session_id = nullif(current_setting('jwt.claims.session_id', true), '')::uuid
  )
  order by r.created desc
  limit 1;
$_$;


--
-- Name: FUNCTION subject_latest_response(subject sg_public.subject); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public.subject_latest_response(subject sg_public.subject) IS 'Get the latest response from the user on the given subject.';


--
-- Name: subject_learned(sg_public.subject); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.subject_learned(subject sg_public.subject) RETURNS real
    LANGUAGE sql STABLE
    AS $_$
  select case when learned is not null then learned else 0.4 end
  from sg_public.subject_latest_response($1);
$_$;


--
-- Name: FUNCTION subject_learned(subject sg_public.subject); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public.subject_learned(subject sg_public.subject) IS 'Get the latest learned value for the user on the given subject.';


--
-- Name: subject_next_child_subjects(sg_public.subject); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.subject_next_child_subjects(subject sg_public.subject) RETURNS SETOF sg_public.subject
    LANGUAGE sql STABLE
    AS $_$
  with subject as (
    select *
    from sg_public.subject
    where entity_id = $1.entity_id
    limit 1
  ),
  all_subjects as (
    select a.*
    from subject, sg_public.subject_all_child_subjects(subject) a
    union
    select * from subject
  ),
  e (all_subjects) as (select array(select entity_id from all_subjects))
  select s.*
  from all_subjects s, e
  where
    sg_public.subject_child_count(s) = 0
    and sg_public.subject_learned(s) < 0.99
    and not sg_public.subject_has_needed_before(s, e.all_subjects)
    -- TODO support "rewind"... going into out of goals befores
    -- when performance is low.
  order by
    sg_public.subject_all_after_count(s) desc,
    sg_public.subject_card_count(s) desc
  limit 5;
$_$;


--
-- Name: FUNCTION subject_next_child_subjects(subject sg_public.subject); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public.subject_next_child_subjects(subject sg_public.subject) IS 'After I select a main subject, search for suitable child subjects.';


--
-- Name: subject_parent_subjects(sg_public.subject); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.subject_parent_subjects(subject sg_public.subject) RETURNS SETOF sg_public.subject
    LANGUAGE sql STABLE
    AS $_$
  select s.*
  from
    sg_public.subject s,
    sg_public.subject_version_parent_child svpc
  where
    svpc.child_version_id = $1.version_id
    and s.entity_id = svpc.parent_entity_id;
$_$;


--
-- Name: FUNCTION subject_parent_subjects(subject sg_public.subject); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public.subject_parent_subjects(subject sg_public.subject) IS 'Collects the direct parents of the child subject.';


--
-- Name: subject_slug(sg_public.subject); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.subject_slug(subject sg_public.subject) RETURNS text
    LANGUAGE sql STABLE
    AS $$
  select slugify(subject.name);
$$;


--
-- Name: FUNCTION subject_slug(subject sg_public.subject); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public.subject_slug(subject sg_public.subject) IS 'The subject''s name as a slug, for URLs.';


--
-- Name: subject_user_count(sg_public.subject); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.subject_user_count(sg_public.subject) RETURNS bigint
    LANGUAGE sql STABLE STRICT SECURITY DEFINER
    AS $_$
  select count(*)
  from sg_public.user_subject us
  where us.subject_id = $1.entity_id
  and us.user_id is not null;
  -- This function should count all usubjs, not just the current users.
$_$;


--
-- Name: FUNCTION subject_user_count(sg_public.subject); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public.subject_user_count(sg_public.subject) IS 'Count the number of logged in users learning the subject.';


--
-- Name: subjects_by_current_user(); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.subjects_by_current_user() RETURNS SETOF sg_public.subject
    LANGUAGE sql STABLE
    AS $$
  select *
  from sg_public.subject
  where entity_id in (
    select entity_id
    from sg_public.subject_version
    where user_id = nullif(current_setting('jwt.claims.user_id', true), '')::uuid
  );
$$;


--
-- Name: FUNCTION subjects_by_current_user(); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public.subjects_by_current_user() IS 'Select subjects I created or worked on.';


--
-- Name: update_card(uuid, text, text[], uuid, sg_public.card_kind, jsonb); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.update_card(entity_id uuid, name text, tags text[], subject_id uuid, kind sg_public.card_kind, data jsonb) RETURNS sg_public.card_version
    LANGUAGE plpgsql STRICT SECURITY DEFINER
    AS $$
  declare
    xprevious sg_public.card;
    xversion_id uuid;
    xcard_version sg_public.card_version;
  begin
    select * into xprevious
    from sg_public.card_by_entity_id(entity_id);
    if (xprevious is null) then
      raise exception 'No previous version found.' using errcode = 'CF018471';
    end if;
    xversion_id := uuid_generate_v4();
    insert into sg_public.entity_version
    (version_id, entity_kind) values (xversion_id, 'card');
    insert into sg_public.card_version
    (version_id, entity_id, language, previous_id, name, tags, subject_id, kind, data)
    values (xversion_id, entity_id, 'en', xprevious.version_id, name, tags, subject_id, kind, data)
    returning * into xcard_version;
    return xcard_version;
  end;
$$;


--
-- Name: FUNCTION update_card(entity_id uuid, name text, tags text[], subject_id uuid, kind sg_public.card_kind, data jsonb); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public.update_card(entity_id uuid, name text, tags text[], subject_id uuid, kind sg_public.card_kind, data jsonb) IS 'Update an existing card.';


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
-- Name: update_subject(uuid, text, text[], text, uuid[], uuid[]); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.update_subject(entity_id uuid, name text, tags text[], body text, parent uuid[], before uuid[]) RETURNS sg_public.subject_version
    LANGUAGE plpgsql STRICT SECURITY DEFINER
    AS $$
  declare
    xprevious sg_public.subject;
    xversion_id uuid;
    xsubject_version sg_public.subject_version;
  begin
    select * into xprevious
    from sg_public.subject_by_entity_id(entity_id);
    if (xprevious is null) then
      raise exception 'No previous version found.' using errcode = 'B7615F09';
    end if;
    xversion_id := uuid_generate_v4();
    insert into sg_public.entity_version
    (version_id, entity_kind) values (xversion_id, 'subject');
    insert into sg_public.subject_version
    (version_id, previous_version_id, entity_id, language, name, tags, body)
    values (xversion_id, xprevious.version_id, entity_id, xprevious.language, name, tags, body)
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
-- Name: FUNCTION update_subject(entity_id uuid, name text, tags text[], body text, parent uuid[], before uuid[]); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public.update_subject(entity_id uuid, name text, tags text[], body text, parent uuid[], before uuid[]) IS 'Update an existing subject.';


--
-- Name: user_md5_email(sg_public."user"); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.user_md5_email(sg_public."user") RETURNS text
    LANGUAGE sql STABLE STRICT SECURITY DEFINER
    AS $_$
  select md5(lower(trim(email)))
  from sg_private.user
  where user_id = $1.id
  limit 1;
$_$;


--
-- Name: FUNCTION user_md5_email(sg_public."user"); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public.user_md5_email(sg_public."user") IS 'The user''s email address as an MD5 hash, for Gravatars. See https://bit.ly/2F6cR0M';


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
-- Name: user_subject_subject(sg_public.user_subject); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.user_subject_subject(us sg_public.user_subject) RETURNS sg_public.subject
    LANGUAGE sql STABLE
    AS $$
  select s.*
  from sg_public.subject as s
  where s.entity_id = us.subject_id
  limit 1;
$$;


--
-- Name: FUNCTION user_subject_subject(us sg_public.user_subject); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public.user_subject_subject(us sg_public.user_subject) IS 'Gets the subject related to the user subject relation.';


--
-- Name: what_is_sagefy(); Type: FUNCTION; Schema: sg_public; Owner: -
--

CREATE FUNCTION sg_public.what_is_sagefy() RETURNS sg_public.subject
    LANGUAGE sql STABLE
    AS $$
  select *
  from sg_public.subject
  where name ilike '%what is sagefy?%'
  limit 1;
$$;


--
-- Name: FUNCTION what_is_sagefy(); Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON FUNCTION sg_public.what_is_sagefy() IS 'Grab just the single "What is Sagefy?" subject, if it exists.';


--
-- Name: english_unaccent; Type: TEXT SEARCH CONFIGURATION; Schema: public; Owner: -
--

CREATE TEXT SEARCH CONFIGURATION public.english_unaccent (
    PARSER = pg_catalog."default" );

ALTER TEXT SEARCH CONFIGURATION public.english_unaccent
    ADD MAPPING FOR asciiword WITH english_stem;

ALTER TEXT SEARCH CONFIGURATION public.english_unaccent
    ADD MAPPING FOR word WITH public.unaccent, english_stem;

ALTER TEXT SEARCH CONFIGURATION public.english_unaccent
    ADD MAPPING FOR numword WITH simple;

ALTER TEXT SEARCH CONFIGURATION public.english_unaccent
    ADD MAPPING FOR email WITH simple;

ALTER TEXT SEARCH CONFIGURATION public.english_unaccent
    ADD MAPPING FOR url WITH simple;

ALTER TEXT SEARCH CONFIGURATION public.english_unaccent
    ADD MAPPING FOR host WITH simple;

ALTER TEXT SEARCH CONFIGURATION public.english_unaccent
    ADD MAPPING FOR sfloat WITH simple;

ALTER TEXT SEARCH CONFIGURATION public.english_unaccent
    ADD MAPPING FOR version WITH simple;

ALTER TEXT SEARCH CONFIGURATION public.english_unaccent
    ADD MAPPING FOR hword_numpart WITH simple;

ALTER TEXT SEARCH CONFIGURATION public.english_unaccent
    ADD MAPPING FOR hword_part WITH public.unaccent, english_stem;

ALTER TEXT SEARCH CONFIGURATION public.english_unaccent
    ADD MAPPING FOR hword_asciipart WITH english_stem;

ALTER TEXT SEARCH CONFIGURATION public.english_unaccent
    ADD MAPPING FOR numhword WITH simple;

ALTER TEXT SEARCH CONFIGURATION public.english_unaccent
    ADD MAPPING FOR asciihword WITH english_stem;

ALTER TEXT SEARCH CONFIGURATION public.english_unaccent
    ADD MAPPING FOR hword WITH public.unaccent, english_stem;

ALTER TEXT SEARCH CONFIGURATION public.english_unaccent
    ADD MAPPING FOR url_path WITH simple;

ALTER TEXT SEARCH CONFIGURATION public.english_unaccent
    ADD MAPPING FOR file WITH simple;

ALTER TEXT SEARCH CONFIGURATION public.english_unaccent
    ADD MAPPING FOR "float" WITH simple;

ALTER TEXT SEARCH CONFIGURATION public.english_unaccent
    ADD MAPPING FOR "int" WITH simple;

ALTER TEXT SEARCH CONFIGURATION public.english_unaccent
    ADD MAPPING FOR uint WITH simple;


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
-- Name: post; Type: TABLE; Schema: sg_public; Owner: -
--

CREATE TABLE sg_public.post (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    created timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    modified timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    user_id uuid,
    session_id uuid,
    topic_id uuid NOT NULL,
    kind sg_public.post_kind DEFAULT 'post'::sg_public.post_kind NOT NULL,
    body text,
    parent_id uuid,
    response boolean,
    CONSTRAINT post_check CHECK (((kind <> 'vote'::sg_public.post_kind) OR (user_id IS NOT NULL))),
    CONSTRAINT post_check1 CHECK (((kind = 'vote'::sg_public.post_kind) OR (body IS NOT NULL))),
    CONSTRAINT post_check2 CHECK (((kind <> 'vote'::sg_public.post_kind) OR (parent_id IS NOT NULL))),
    CONSTRAINT post_check3 CHECK (((kind <> 'vote'::sg_public.post_kind) OR (response IS NOT NULL))),
    CONSTRAINT user_or_session CHECK (((user_id IS NOT NULL) OR (session_id IS NOT NULL)))
);


--
-- Name: TABLE post; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TABLE sg_public.post IS 'The posts on an entity''s talk page. Belongs to a topic.';


--
-- Name: COLUMN post.id; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.post.id IS 'The ID of the post.';


--
-- Name: COLUMN post.created; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.post.created IS 'When the user created the post.';


--
-- Name: COLUMN post.modified; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.post.modified IS 'When the post last changed.';


--
-- Name: COLUMN post.user_id; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.post.user_id IS 'The user who created the post.';


--
-- Name: COLUMN post.session_id; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.post.session_id IS 'The logged out user who created the post.';


--
-- Name: COLUMN post.topic_id; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.post.topic_id IS 'The topic the post belongs to.';


--
-- Name: COLUMN post.kind; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.post.kind IS 'The kind of post (post, proposal, vote).';


--
-- Name: COLUMN post.body; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.post.body IS 'The body or main content of the post.';


--
-- Name: COLUMN post.parent_id; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.post.parent_id IS 'If the post is a reply, which post it replies to.';


--
-- Name: COLUMN post.response; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.post.response IS 'If the post is a vote, yes/no on approving.';


--
-- Name: post_entity_version; Type: TABLE; Schema: sg_public; Owner: -
--

CREATE TABLE sg_public.post_entity_version (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    created timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    modified timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    post_id uuid NOT NULL,
    version_id uuid NOT NULL,
    entity_kind sg_public.entity_kind NOT NULL
);


--
-- Name: TABLE post_entity_version; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TABLE sg_public.post_entity_version IS 'A join table between a proposal (post) and its entity versions.';


--
-- Name: COLUMN post_entity_version.id; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.post_entity_version.id IS 'The relationship ID.';


--
-- Name: COLUMN post_entity_version.created; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.post_entity_version.created IS 'When a user created this post.';


--
-- Name: COLUMN post_entity_version.modified; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.post_entity_version.modified IS 'When a user last modified this post.';


--
-- Name: COLUMN post_entity_version.post_id; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.post_entity_version.post_id IS 'The post ID.';


--
-- Name: COLUMN post_entity_version.version_id; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.post_entity_version.version_id IS 'The entity ID of the entity version.';


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
-- Name: topic; Type: TABLE; Schema: sg_public; Owner: -
--

CREATE TABLE sg_public.topic (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    created timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    modified timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    user_id uuid,
    session_id uuid,
    name text NOT NULL,
    entity_id uuid NOT NULL,
    entity_kind sg_public.entity_kind NOT NULL,
    CONSTRAINT user_or_session CHECK (((user_id IS NOT NULL) OR (session_id IS NOT NULL)))
);


--
-- Name: TABLE topic; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TABLE sg_public.topic IS 'The topics on an entity''s talk page.';


--
-- Name: COLUMN topic.id; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.topic.id IS 'The public ID of the topic.';


--
-- Name: COLUMN topic.created; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.topic.created IS 'When the user created the topic.';


--
-- Name: COLUMN topic.modified; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.topic.modified IS 'When the user last modified the topic.';


--
-- Name: COLUMN topic.user_id; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.topic.user_id IS 'The user who created the topic.';


--
-- Name: COLUMN topic.session_id; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.topic.session_id IS 'The logged out person who created the topic.';


--
-- Name: COLUMN topic.name; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.topic.name IS 'The name of the topic.';


--
-- Name: COLUMN topic.entity_id; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.topic.entity_id IS 'The entity the topic belongs to.';


--
-- Name: COLUMN topic.entity_kind; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON COLUMN sg_public.topic.entity_kind IS 'The kind of entity the topic belongs to.';


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
-- Name: post_entity_version post_entity_version_pkey; Type: CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.post_entity_version
    ADD CONSTRAINT post_entity_version_pkey PRIMARY KEY (id);


--
-- Name: post_entity_version post_entity_version_post_id_version_id_key; Type: CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.post_entity_version
    ADD CONSTRAINT post_entity_version_post_id_version_id_key UNIQUE (post_id, version_id);


--
-- Name: post post_pkey; Type: CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.post
    ADD CONSTRAINT post_pkey PRIMARY KEY (id);


--
-- Name: response response_pkey; Type: CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.response
    ADD CONSTRAINT response_pkey PRIMARY KEY (id);


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
-- Name: topic topic_pkey; Type: CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.topic
    ADD CONSTRAINT topic_pkey PRIMARY KEY (id);


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
-- Name: card_version_created_idx; Type: INDEX; Schema: sg_public; Owner: -
--

CREATE INDEX card_version_created_idx ON sg_public.card_version USING btree (created);


--
-- Name: card_version_distinct_idx; Type: INDEX; Schema: sg_public; Owner: -
--

CREATE INDEX card_version_distinct_idx ON sg_public.card_version USING btree (entity_id, created DESC) WHERE (status = 'accepted'::sg_public.entity_status);


--
-- Name: card_version_entity_id_idx; Type: INDEX; Schema: sg_public; Owner: -
--

CREATE INDEX card_version_entity_id_idx ON sg_public.card_version USING btree (entity_id);


--
-- Name: card_version_previous_id_idx; Type: INDEX; Schema: sg_public; Owner: -
--

CREATE INDEX card_version_previous_id_idx ON sg_public.card_version USING btree (previous_id);


--
-- Name: card_version_subject_id_idx; Type: INDEX; Schema: sg_public; Owner: -
--

CREATE INDEX card_version_subject_id_idx ON sg_public.card_version USING btree (subject_id);


--
-- Name: card_version_user_id_idx; Type: INDEX; Schema: sg_public; Owner: -
--

CREATE INDEX card_version_user_id_idx ON sg_public.card_version USING btree (user_id);


--
-- Name: post_created_idx; Type: INDEX; Schema: sg_public; Owner: -
--

CREATE INDEX post_created_idx ON sg_public.post USING btree (created);


--
-- Name: post_entity_version_version_id_entity_kind_idx; Type: INDEX; Schema: sg_public; Owner: -
--

CREATE INDEX post_entity_version_version_id_entity_kind_idx ON sg_public.post_entity_version USING btree (version_id, entity_kind);


--
-- Name: post_parent_id_idx; Type: INDEX; Schema: sg_public; Owner: -
--

CREATE INDEX post_parent_id_idx ON sg_public.post USING btree (parent_id);


--
-- Name: post_topic_id_idx; Type: INDEX; Schema: sg_public; Owner: -
--

CREATE INDEX post_topic_id_idx ON sg_public.post USING btree (topic_id);


--
-- Name: post_user_id_idx; Type: INDEX; Schema: sg_public; Owner: -
--

CREATE INDEX post_user_id_idx ON sg_public.post USING btree (user_id);


--
-- Name: post_vote_unique_idx; Type: INDEX; Schema: sg_public; Owner: -
--

CREATE UNIQUE INDEX post_vote_unique_idx ON sg_public.post USING btree (user_id, parent_id) WHERE (kind = 'vote'::sg_public.post_kind);


--
-- Name: response_card_id_idx; Type: INDEX; Schema: sg_public; Owner: -
--

CREATE INDEX response_card_id_idx ON sg_public.response USING btree (card_id);


--
-- Name: response_subject_id_idx; Type: INDEX; Schema: sg_public; Owner: -
--

CREATE INDEX response_subject_id_idx ON sg_public.response USING btree (subject_id);


--
-- Name: response_user_id_idx; Type: INDEX; Schema: sg_public; Owner: -
--

CREATE INDEX response_user_id_idx ON sg_public.response USING btree (user_id);


--
-- Name: search_card_idx; Type: INDEX; Schema: sg_public; Owner: -
--

CREATE INDEX search_card_idx ON sg_public.card_version USING gin (to_tsvector('public.english_unaccent'::regconfig, public.text_concat_ws(' '::text, VARIADIC ARRAY[name, public.text_array_to_text(tags), (data)::text])));


--
-- Name: search_subject_idx; Type: INDEX; Schema: sg_public; Owner: -
--

CREATE INDEX search_subject_idx ON sg_public.subject_version USING gin (to_tsvector('public.english_unaccent'::regconfig, public.text_concat_ws(' '::text, VARIADIC ARRAY[name, public.text_array_to_text(tags), body])));


--
-- Name: subject_version_before_after_after_version_id_idx; Type: INDEX; Schema: sg_public; Owner: -
--

CREATE INDEX subject_version_before_after_after_version_id_idx ON sg_public.subject_version_before_after USING btree (after_version_id);


--
-- Name: subject_version_before_after_before_entity_id_idx; Type: INDEX; Schema: sg_public; Owner: -
--

CREATE INDEX subject_version_before_after_before_entity_id_idx ON sg_public.subject_version_before_after USING btree (before_entity_id);


--
-- Name: subject_version_created_idx; Type: INDEX; Schema: sg_public; Owner: -
--

CREATE INDEX subject_version_created_idx ON sg_public.subject_version USING btree (created);


--
-- Name: subject_version_distinct_idx; Type: INDEX; Schema: sg_public; Owner: -
--

CREATE INDEX subject_version_distinct_idx ON sg_public.subject_version USING btree (entity_id, created DESC) WHERE (status = 'accepted'::sg_public.entity_status);


--
-- Name: subject_version_entity_id_idx; Type: INDEX; Schema: sg_public; Owner: -
--

CREATE INDEX subject_version_entity_id_idx ON sg_public.subject_version USING btree (entity_id);


--
-- Name: subject_version_parent_child_child_version_id_idx; Type: INDEX; Schema: sg_public; Owner: -
--

CREATE INDEX subject_version_parent_child_child_version_id_idx ON sg_public.subject_version_parent_child USING btree (child_version_id);


--
-- Name: subject_version_parent_child_parent_entity_id_idx; Type: INDEX; Schema: sg_public; Owner: -
--

CREATE INDEX subject_version_parent_child_parent_entity_id_idx ON sg_public.subject_version_parent_child USING btree (parent_entity_id);


--
-- Name: subject_version_previous_version_id_idx; Type: INDEX; Schema: sg_public; Owner: -
--

CREATE INDEX subject_version_previous_version_id_idx ON sg_public.subject_version USING btree (previous_version_id);


--
-- Name: subject_version_user_id_idx; Type: INDEX; Schema: sg_public; Owner: -
--

CREATE INDEX subject_version_user_id_idx ON sg_public.subject_version USING btree (user_id);


--
-- Name: topic_created_idx; Type: INDEX; Schema: sg_public; Owner: -
--

CREATE INDEX topic_created_idx ON sg_public.topic USING btree (created);


--
-- Name: topic_entity_id_entity_kind_idx; Type: INDEX; Schema: sg_public; Owner: -
--

CREATE INDEX topic_entity_id_entity_kind_idx ON sg_public.topic USING btree (entity_id, entity_kind);


--
-- Name: topic_entity_id_idx; Type: INDEX; Schema: sg_public; Owner: -
--

CREATE INDEX topic_entity_id_idx ON sg_public.topic USING btree (entity_id);


--
-- Name: topic_user_id_idx; Type: INDEX; Schema: sg_public; Owner: -
--

CREATE INDEX topic_user_id_idx ON sg_public.topic USING btree (user_id);


--
-- Name: user_subject_subject_id_idx; Type: INDEX; Schema: sg_public; Owner: -
--

CREATE INDEX user_subject_subject_id_idx ON sg_public.user_subject USING btree (subject_id);


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
-- Name: card_version insert_card_version_status; Type: TRIGGER; Schema: sg_public; Owner: -
--

CREATE TRIGGER insert_card_version_status BEFORE INSERT ON sg_public.card_version FOR EACH ROW EXECUTE PROCEDURE sg_private.insert_card_version_status();


--
-- Name: TRIGGER insert_card_version_status ON card_version; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TRIGGER insert_card_version_status ON sg_public.card_version IS 'When inserting a new card, automatically set the status to accepted.';


--
-- Name: card_version insert_card_version_user_or_session; Type: TRIGGER; Schema: sg_public; Owner: -
--

CREATE TRIGGER insert_card_version_user_or_session BEFORE INSERT ON sg_public.card_version FOR EACH ROW EXECUTE PROCEDURE sg_private.insert_user_or_session();


--
-- Name: TRIGGER insert_card_version_user_or_session ON card_version; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TRIGGER insert_card_version_user_or_session ON sg_public.card_version IS 'Automatically add the user_id or session_id.';


--
-- Name: post insert_post_user_id; Type: TRIGGER; Schema: sg_public; Owner: -
--

CREATE TRIGGER insert_post_user_id BEFORE INSERT ON sg_public.post FOR EACH ROW EXECUTE PROCEDURE sg_private.insert_user_or_session();


--
-- Name: TRIGGER insert_post_user_id ON post; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TRIGGER insert_post_user_id ON sg_public.post IS 'Whenever I make a new post, auto fill the `user_id` column';


--
-- Name: post insert_post_verify; Type: TRIGGER; Schema: sg_public; Owner: -
--

CREATE TRIGGER insert_post_verify BEFORE INSERT ON sg_public.post FOR EACH ROW EXECUTE PROCEDURE sg_private.verify_post();


--
-- Name: TRIGGER insert_post_verify ON post; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TRIGGER insert_post_verify ON sg_public.post IS 'Whenever I make a new post, check that the post is valid.';


--
-- Name: response insert_response_score; Type: TRIGGER; Schema: sg_public; Owner: -
--

CREATE TRIGGER insert_response_score BEFORE INSERT ON sg_public.response FOR EACH ROW EXECUTE PROCEDURE sg_private.score_response();


--
-- Name: TRIGGER insert_response_score ON response; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TRIGGER insert_response_score ON sg_public.response IS 'After I respond to a card, score the result and update model.';


--
-- Name: response insert_response_user_or_session; Type: TRIGGER; Schema: sg_public; Owner: -
--

CREATE TRIGGER insert_response_user_or_session BEFORE INSERT ON sg_public.response FOR EACH ROW EXECUTE PROCEDURE sg_private.insert_user_or_session();


--
-- Name: TRIGGER insert_response_user_or_session ON response; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TRIGGER insert_response_user_or_session ON sg_public.response IS 'Whenever I make a new response, auto fill the `user_id` column';


--
-- Name: subject_version insert_subject_version_auto_user_subject; Type: TRIGGER; Schema: sg_public; Owner: -
--

CREATE TRIGGER insert_subject_version_auto_user_subject AFTER INSERT ON sg_public.subject_version FOR EACH ROW EXECUTE PROCEDURE sg_private.subject_auto_user_subject();


--
-- Name: TRIGGER insert_subject_version_auto_user_subject ON subject_version; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TRIGGER insert_subject_version_auto_user_subject ON sg_public.subject_version IS 'Whenever I make a new subject version, add me as a learner.';


--
-- Name: subject_version insert_subject_version_name; Type: TRIGGER; Schema: sg_public; Owner: -
--

CREATE TRIGGER insert_subject_version_name BEFORE INSERT ON sg_public.subject_version FOR EACH ROW EXECUTE PROCEDURE sg_private.subject_unique_name();


--
-- Name: TRIGGER insert_subject_version_name ON subject_version; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TRIGGER insert_subject_version_name ON sg_public.subject_version IS 'Ensure new subject versions have a unique name.';


--
-- Name: subject_version insert_subject_version_status; Type: TRIGGER; Schema: sg_public; Owner: -
--

CREATE TRIGGER insert_subject_version_status BEFORE INSERT ON sg_public.subject_version FOR EACH ROW EXECUTE PROCEDURE sg_private.insert_subject_version_status();


--
-- Name: TRIGGER insert_subject_version_status ON subject_version; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TRIGGER insert_subject_version_status ON sg_public.subject_version IS 'When inserting a new subject, automatically set the status to accepted.';


--
-- Name: subject_version insert_subject_version_user_or_session; Type: TRIGGER; Schema: sg_public; Owner: -
--

CREATE TRIGGER insert_subject_version_user_or_session BEFORE INSERT ON sg_public.subject_version FOR EACH ROW EXECUTE PROCEDURE sg_private.insert_user_or_session();


--
-- Name: TRIGGER insert_subject_version_user_or_session ON subject_version; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TRIGGER insert_subject_version_user_or_session ON sg_public.subject_version IS 'Automatically add the user_id or session_id.';


--
-- Name: topic insert_topic_user_id; Type: TRIGGER; Schema: sg_public; Owner: -
--

CREATE TRIGGER insert_topic_user_id BEFORE INSERT ON sg_public.topic FOR EACH ROW EXECUTE PROCEDURE sg_private.insert_user_or_session();


--
-- Name: TRIGGER insert_topic_user_id ON topic; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TRIGGER insert_topic_user_id ON sg_public.topic IS 'Whenever I make a new topic, auto fill the `user_id` column';


--
-- Name: user_subject insert_user_subject_user_or_session; Type: TRIGGER; Schema: sg_public; Owner: -
--

CREATE TRIGGER insert_user_subject_user_or_session BEFORE INSERT ON sg_public.user_subject FOR EACH ROW EXECUTE PROCEDURE sg_private.insert_user_or_session();


--
-- Name: TRIGGER insert_user_subject_user_or_session ON user_subject; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TRIGGER insert_user_subject_user_or_session ON sg_public.user_subject IS 'Whenever I make a new user subject, auto fill the `user_id` or `session_id` field.';


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
-- Name: post_entity_version update_post_entity_version_modified; Type: TRIGGER; Schema: sg_public; Owner: -
--

CREATE TRIGGER update_post_entity_version_modified BEFORE UPDATE ON sg_public.post_entity_version FOR EACH ROW EXECUTE PROCEDURE sg_private.update_modified_column();


--
-- Name: TRIGGER update_post_entity_version_modified ON post_entity_version; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TRIGGER update_post_entity_version_modified ON sg_public.post_entity_version IS 'Whenever a post entity version changes, update the `modified` column.';


--
-- Name: post update_post_modified; Type: TRIGGER; Schema: sg_public; Owner: -
--

CREATE TRIGGER update_post_modified BEFORE UPDATE ON sg_public.post FOR EACH ROW EXECUTE PROCEDURE sg_private.update_modified_column();


--
-- Name: TRIGGER update_post_modified ON post; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TRIGGER update_post_modified ON sg_public.post IS 'Whenever a post changes, update the `modified` column.';


--
-- Name: post update_post_verify; Type: TRIGGER; Schema: sg_public; Owner: -
--

CREATE TRIGGER update_post_verify BEFORE UPDATE ON sg_public.post FOR EACH ROW EXECUTE PROCEDURE sg_private.verify_post();


--
-- Name: TRIGGER update_post_verify ON post; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TRIGGER update_post_verify ON sg_public.post IS 'Whenever I make a new post, check that the post is valid.';


--
-- Name: response update_response_modified; Type: TRIGGER; Schema: sg_public; Owner: -
--

CREATE TRIGGER update_response_modified BEFORE UPDATE ON sg_public.response FOR EACH ROW EXECUTE PROCEDURE sg_private.update_modified_column();


--
-- Name: TRIGGER update_response_modified ON response; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TRIGGER update_response_modified ON sg_public.response IS 'Whenever a response changes, update the `modified` column.';


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
-- Name: topic update_topic_modified; Type: TRIGGER; Schema: sg_public; Owner: -
--

CREATE TRIGGER update_topic_modified BEFORE UPDATE ON sg_public.topic FOR EACH ROW EXECUTE PROCEDURE sg_private.update_modified_column();


--
-- Name: TRIGGER update_topic_modified ON topic; Type: COMMENT; Schema: sg_public; Owner: -
--

COMMENT ON TRIGGER update_topic_modified ON sg_public.topic IS 'Whenever a topic changes, update the `modified` column.';


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
-- Name: post_entity_version post_entity_version_post_id_fkey; Type: FK CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.post_entity_version
    ADD CONSTRAINT post_entity_version_post_id_fkey FOREIGN KEY (post_id) REFERENCES sg_public.post(id);


--
-- Name: post_entity_version post_entity_version_version_id_fkey; Type: FK CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.post_entity_version
    ADD CONSTRAINT post_entity_version_version_id_fkey FOREIGN KEY (version_id, entity_kind) REFERENCES sg_public.entity_version(version_id, entity_kind);


--
-- Name: post post_parent_id_fkey; Type: FK CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.post
    ADD CONSTRAINT post_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES sg_public.post(id);


--
-- Name: post post_topic_id_fkey; Type: FK CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.post
    ADD CONSTRAINT post_topic_id_fkey FOREIGN KEY (topic_id) REFERENCES sg_public.topic(id);


--
-- Name: post post_user_id_fkey; Type: FK CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.post
    ADD CONSTRAINT post_user_id_fkey FOREIGN KEY (user_id) REFERENCES sg_public."user"(id);


--
-- Name: response response_card_id_fkey; Type: FK CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.response
    ADD CONSTRAINT response_card_id_fkey FOREIGN KEY (card_id) REFERENCES sg_public.card_entity(entity_id);


--
-- Name: response response_subject_id_fkey; Type: FK CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.response
    ADD CONSTRAINT response_subject_id_fkey FOREIGN KEY (subject_id) REFERENCES sg_public.subject_entity(entity_id);


--
-- Name: response response_user_id_fkey; Type: FK CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.response
    ADD CONSTRAINT response_user_id_fkey FOREIGN KEY (user_id) REFERENCES sg_public."user"(id);


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
-- Name: topic topic_entity_id_fkey; Type: FK CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.topic
    ADD CONSTRAINT topic_entity_id_fkey FOREIGN KEY (entity_id, entity_kind) REFERENCES sg_public.entity(entity_id, entity_kind);


--
-- Name: topic topic_user_id_fkey; Type: FK CONSTRAINT; Schema: sg_public; Owner: -
--

ALTER TABLE ONLY sg_public.topic
    ADD CONSTRAINT topic_user_id_fkey FOREIGN KEY (user_id) REFERENCES sg_public."user"(id);


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
-- Name: post delete_post_admin; Type: POLICY; Schema: sg_public; Owner: -
--

CREATE POLICY delete_post_admin ON sg_public.post FOR DELETE TO sg_admin USING (true);


--
-- Name: topic delete_topic_admin; Type: POLICY; Schema: sg_public; Owner: -
--

CREATE POLICY delete_topic_admin ON sg_public.topic FOR DELETE TO sg_admin USING (true);


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

CREATE POLICY delete_user_subject ON sg_public.user_subject FOR DELETE TO sg_anonymous, sg_user, sg_admin USING (((user_id = (NULLIF(current_setting('jwt.claims.user_id'::text, true), ''::text))::uuid) OR (session_id = (NULLIF(current_setting('jwt.claims.session_id'::text, true), ''::text))::uuid)));


--
-- Name: post insert_post; Type: POLICY; Schema: sg_public; Owner: -
--

CREATE POLICY insert_post ON sg_public.post FOR INSERT WITH CHECK (true);


--
-- Name: response insert_response; Type: POLICY; Schema: sg_public; Owner: -
--

CREATE POLICY insert_response ON sg_public.response FOR INSERT TO sg_anonymous, sg_user, sg_admin WITH CHECK (true);


--
-- Name: topic insert_topic; Type: POLICY; Schema: sg_public; Owner: -
--

CREATE POLICY insert_topic ON sg_public.topic FOR INSERT WITH CHECK (true);


--
-- Name: user_subject insert_user_subject; Type: POLICY; Schema: sg_public; Owner: -
--

CREATE POLICY insert_user_subject ON sg_public.user_subject FOR INSERT TO sg_anonymous, sg_user, sg_admin WITH CHECK (true);


--
-- Name: post; Type: ROW SECURITY; Schema: sg_public; Owner: -
--

ALTER TABLE sg_public.post ENABLE ROW LEVEL SECURITY;

--
-- Name: response; Type: ROW SECURITY; Schema: sg_public; Owner: -
--

ALTER TABLE sg_public.response ENABLE ROW LEVEL SECURITY;

--
-- Name: post select_post; Type: POLICY; Schema: sg_public; Owner: -
--

CREATE POLICY select_post ON sg_public.post FOR SELECT USING (true);


--
-- Name: response select_response; Type: POLICY; Schema: sg_public; Owner: -
--

CREATE POLICY select_response ON sg_public.response FOR SELECT TO sg_anonymous, sg_user, sg_admin USING (((user_id = (NULLIF(current_setting('jwt.claims.user_id'::text, true), ''::text))::uuid) OR (session_id = (NULLIF(current_setting('jwt.claims.session_id'::text, true), ''::text))::uuid)));


--
-- Name: topic select_topic; Type: POLICY; Schema: sg_public; Owner: -
--

CREATE POLICY select_topic ON sg_public.topic FOR SELECT USING (true);


--
-- Name: user select_user; Type: POLICY; Schema: sg_public; Owner: -
--

CREATE POLICY select_user ON sg_public."user" FOR SELECT USING (true);


--
-- Name: user_subject select_user_subject; Type: POLICY; Schema: sg_public; Owner: -
--

CREATE POLICY select_user_subject ON sg_public.user_subject FOR SELECT TO sg_anonymous, sg_user, sg_admin USING (((user_id = (NULLIF(current_setting('jwt.claims.user_id'::text, true), ''::text))::uuid) OR (session_id = (NULLIF(current_setting('jwt.claims.session_id'::text, true), ''::text))::uuid)));


--
-- Name: topic; Type: ROW SECURITY; Schema: sg_public; Owner: -
--

ALTER TABLE sg_public.topic ENABLE ROW LEVEL SECURITY;

--
-- Name: post update_post; Type: POLICY; Schema: sg_public; Owner: -
--

CREATE POLICY update_post ON sg_public.post FOR UPDATE TO sg_user USING ((user_id = (NULLIF(current_setting('jwt.claims.user_id'::text, true), ''::text))::uuid));


--
-- Name: post update_post_admin; Type: POLICY; Schema: sg_public; Owner: -
--

CREATE POLICY update_post_admin ON sg_public.post FOR UPDATE TO sg_admin USING (true);


--
-- Name: topic update_topic; Type: POLICY; Schema: sg_public; Owner: -
--

CREATE POLICY update_topic ON sg_public.topic FOR UPDATE TO sg_user USING ((user_id = (NULLIF(current_setting('jwt.claims.user_id'::text, true), ''::text))::uuid));


--
-- Name: topic update_topic_admin; Type: POLICY; Schema: sg_public; Owner: -
--

CREATE POLICY update_topic_admin ON sg_public.topic FOR UPDATE TO sg_admin USING (true);


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
    ('20190322230728'),
    ('20190328211620'),
    ('20190401185105'),
    ('20190403175843'),
    ('20190403183651'),
    ('20190409203511'),
    ('20190411224126'),
    ('20190412211807'),
    ('20190418165040'),
    ('20190524205800'),
    ('20190529204020'),
    ('20190606175104'),
    ('20190715015859'),
    ('20190716223347'),
    ('20190718184132'),
    ('20190718190417'),
    ('20190724165943'),
    ('20190726171316'),
    ('20190729222214'),
    ('20190730184403'),
    ('20190731013731'),
    ('20190803024055'),
    ('20190803033630'),
    ('20190803044152'),
    ('20190821170318'),
    ('20190821230739'),
    ('20190821233703'),
    ('20190822150444');
