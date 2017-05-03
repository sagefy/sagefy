/*
    This is a part of a proposed changed back to PostgreSQL from RethinkDB.
    This schema is still evolving.
    No decision has been made.

TO think about:
    user settings
    post entity_versions
    set members
    c_params guess/slip

    ENSURE is UTF-8
*/


CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.modified = now();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TABLE users (
    id          char(24)        PRIMARY KEY,
    created     timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified    timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name        text            NOT NULL UNIQUE,
    email       text            NOT NULL UNIQUE,
    password    varchar(60)     NOT NULL,
    settings    jsonb           NOT NULL
);

CREATE TRIGGER update_users_modified
    BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE PROCEDURE update_modified_column();

/* NB set_ids >>> set_id */

CREATE TABLE users_sets (
    id          char(24)        PRIMARY KEY,
    created     timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified    timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id     char(24)        NOT NULL REFERENCES users (id),
    set_id      char(24)        NOT NULL REFERENCES sets (id)
);

CREATE TRIGGER update_users_sets_modified
    BEFORE UPDATE ON users_sets
    FOR EACH ROW EXECUTE PROCEDURE update_modified_column();

CREATE TYPE entity_kind AS ENUM(
    'card',
    'unit',
    'set'
);

CREATE TABLE topics (
    id          char(24)        PRIMARY KEY,
    created     timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified    timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id     char(24)        NOT NULL REFERENCES users (id),
    name        text            NOT NULL,
    entity_id   char(24)        NOT NULL,  /* cant ref non-unique */
    entity_kind entity_kind     NOT NULL
);

CREATE TRIGGER update_topics_modified
    BEFORE UPDATE ON topics
    FOR EACH ROW EXECUTE PROCEDURE update_modified_column();

CREATE TYPE post_kind as ENUM(
    'post',
    'proposal',
    'vote'
);

CREATE TABLE posts (
    id          char(24)        PRIMARY KEY,
    created     timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified    timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id     char(24)        NOT NULL REFERENCES users (id),
    topic_id    char(24)        NOT NULL REFERENCES topics (id),
    kind        post_kind       NOT NULL DEFAULT 'post',
    body        text            NULL
        CHECK (kind = 'vote' OR body IS NOT NULL),
    replies_to_id char(24)      NULL REFERENCES posts (id)
        CHECK (kind <> 'vote' OR replies_to_id IS NOT NULL),
    entity_versions jsonb       NULL
        CHECK (kind <> 'proposal' or entity_versions IS NOT NULL),
    response    boolean         NULL
        CHECK (kind <> 'vote' OR response IS NOT NULL)
);

CREATE TRIGGER update_posts_modified
    BEFORE UPDATE ON posts
    FOR EACH ROW EXECUTE PROCEDURE update_modified_column();

CREATE TYPE notice_kind as ENUM(
    'create_topic',
    'create_proposal',
    'block_proposal',
    'decline_proposal',
    'accept_proposal',
    'create_post',
    'come_back'
);

CREATE TABLE notices (
    id          char(24)        PRIMARY KEY,
    created     timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified    timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id     char(24)        NOT NULL REFERENCES users (id),
    kind        notice_kind     NOT NULL,
    data        jsonb           NOT NULL,
    read        boolean         NOT NULL DEFAULT FALSE,
    tags        text[]          NULL DEFAULT array[]::text[]
);

CREATE TRIGGER update_notices_modified
    BEFORE UPDATE ON notices
    FOR EACH ROW EXECUTE PROCEDURE update_modified_column();

CREATE TYPE follow_kind AS ENUM(
    'card',
    'unit',
    'set',
    'topic'
);

CREATE TABLE follows (
    id          char(24)        PRIMARY KEY,
    created     timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified    timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id     char(24)        NOT NULL REFERENCES users (id),
    entity_id   char(24)        NOT NULL, /* cant ref non-unique */
    entity_kind follow_kind     NOT NULL
);

CREATE TRIGGER update_follows_modified
    BEFORE UPDATE ON follows
    FOR EACH ROW EXECUTE PROCEDURE update_modified_column();

CREATE TYPE entity_status AS ENUM(
    'pending',
    'blocked',
    'declined',
    'accepted'
);

CREATE TABLE units (
    version_id  char(24)        PRIMARY KEY,
    created     timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified    timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    entity_id   char(24)        NOT NULL, /* non-unique */
    previous_id char(24)        NULL REFERENCES units (version_id),
    language    varchar(5)      NOT NULL DEFAULT 'en',
    name        text            NOT NULL,
    status      entity_status   NOT NULL DEFAULT 'pending',
    available   boolean         NOT NULL DEFAULT TRUE,
    tags        text[]          NULL DEFAULT array[]::text[],
    /* and the rest.... */
    body        text            NOT NULL,
    require_ids varchar(24)[]   NOT NULL  /* cant ref non-unique, no ELEMENT */
);

CREATE TRIGGER update_units_modified
    BEFORE UPDATE ON units
    FOR EACH ROW EXECUTE PROCEDURE update_modified_column();

CREATE TABLE sets (
    version_id  char(24)        PRIMARY KEY,
    created     timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified    timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    entity_id   char(24)        NOT NULL, /* non-unique */
    previous_id char(24)        NULL REFERENCES sets (version_id),
    language    varchar(5)      NOT NULL DEFAULT 'en',
    name        text            NOT NULL,
    status      entity_status   NOT NULL DEFAULT 'pending',
    available   boolean         NOT NULL DEFAULT TRUE,
    tags        text[]          NULL DEFAULT array[]::text[],
    /* and the rest.... */
    body        text            NOT NULL,
    members     jsonb           NOT NULL
);

CREATE TRIGGER update_sets_modified
    BEFORE UPDATE ON sets
    FOR EACH ROW EXECUTE PROCEDURE update_modified_column();

CREATE TYPE card_kind AS ENUM(
    'video',
    'choice'
);

CREATE TABLE cards (
    version_id  char(24)        PRIMARY KEY,
    created     timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified    timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    entity_id   char(24)        NOT NULL, /* non-unique */
    previous_id char(24)        NULL REFERENCES cards (version_id),
    language    varchar(5)      NOT NULL DEFAULT 'en',
    name        text            NOT NULL,
    status      entity_status   NOT NULL DEFAULT 'pending',
    available   boolean         NOT NULL DEFAULT TRUE,
    tags        text[]          NULL DEFAULT array[]::text[],
    /* and the rest.... */
    unit_id     char(24)        NOT NULL, /* cant ref non-unique */
    require_ids char(24)[]      NOT NULL, /* cant ref non-unique, no ELEMENT */
    kind        card_kind       NOT NULL,
    data        jsonb           NOT NULL
);

CREATE TRIGGER update_cards_modified
    BEFORE UPDATE ON cards
    FOR EACH ROW EXECUTE PROCEDURE update_modified_column();

CREATE TABLE cards_parameters (
    id          char(24)        PRIMARY KEY,
    created     timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified    timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    entity_id   char(24)        NOT NULL UNIQUE, /* cant ref non-unique */
    guess_distribution  jsonb   NOT NULL,
    slip_distribution   jsonb   NOT NULL
);

CREATE TRIGGER update_cards_parameters_modified
    BEFORE UPDATE ON cards_parameters
    FOR EACH ROW EXECUTE PROCEDURE update_modified_column();

CREATE TABLE responses (
    id          char(24)        PRIMARY KEY,
    created     timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified    timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id     char(24)        NOT NULL REFERENCES users (id),
    card_id     char(24)        NOT NULL, /* cant ref non-unique */
    unit_id     char(24)        NOT NULL, /* cant ref non-unique */
    response    text            NOT NULL,
    score       double precision NOT NULL
        CHECK (score >= 0 AND score <= 1),
    learned     double precision NOT NULL
        CHECK (score >= 0 AND score <= 1)
);

CREATE TRIGGER update_responses_modified
    BEFORE UPDATE ON responses
    FOR EACH ROW EXECUTE PROCEDURE update_modified_column();
