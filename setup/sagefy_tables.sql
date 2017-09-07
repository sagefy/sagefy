/* ENSURE is UTF-8 */

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TYPE entity_kind AS ENUM(
    'card',
    'unit',
    'subject'
);

CREATE TYPE post_kind as ENUM(
    'post',
    'proposal',
    'vote'
);

CREATE TYPE notice_kind as ENUM(
    'create_topic',
    'create_proposal',
    'block_proposal',
    'decline_proposal',
    'accept_proposal',
    'create_post',
    'come_back'
);

CREATE TYPE follow_kind AS ENUM(
    'card',
    'unit',
    'subject',
    'topic'
);

CREATE TYPE entity_status AS ENUM(
    'pending',
    'blocked',
    'declined',
    'accepted'
);

CREATE TYPE card_kind AS ENUM(
    'video',
    'choice'
);

CREATE TABLE users (
    id          uuid            PRIMARY KEY DEFAULT uuid_generate_v4(),
    created     timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified    timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name        text            NOT NULL UNIQUE,
    email       text            NOT NULL UNIQUE
        CONSTRAINT email_check CHECK (email ~* '^\S+@\S+\.\S+$'),
    password    varchar(60)     NOT NULL
        CONSTRAINT pass_check CHECK (password ~* '^\$2a\$.*$'),
    settings    jsonb           NOT NULL
        /* jsonb?: add new settings without alter table */
);

CREATE TABLE topics (
    id          uuid            PRIMARY KEY DEFAULT uuid_generate_v4(),
    created     timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified    timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id     uuid            NOT NULL REFERENCES users (id),
    name        text            NOT NULL,
    entity_id   uuid            NOT NULL,  /* ISSUE cant ref across tables */
    entity_kind entity_kind     NOT NULL
);

CREATE TABLE posts (
    id          uuid            PRIMARY KEY DEFAULT uuid_generate_v4(),
    created     timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified    timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id     uuid            NOT NULL REFERENCES users (id),
    topic_id    uuid            NOT NULL REFERENCES topics (id),
    kind        post_kind       NOT NULL DEFAULT 'post',
    body        text            NULL
        CHECK (kind = 'vote' OR body IS NOT NULL),
    replies_to_id uuid          NULL REFERENCES posts (id)
        CHECK (kind <> 'vote' OR replies_to_id IS NOT NULL),
    entity_versions jsonb       NULL
        CHECK (kind <> 'proposal' or entity_versions IS NOT NULL),
        /* jsonb?: ISSUE cant ref, cant enum composite */
    response    boolean         NULL
        CHECK (kind <> 'vote' OR response IS NOT NULL)
);

CREATE UNIQUE INDEX posts_vote_unique_idx ON posts (user_id, replies_to_id) WHERE kind = 'vote';

CREATE TABLE notices (
    id          uuid            PRIMARY KEY DEFAULT uuid_generate_v4(),
    created     timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified    timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id     uuid            NOT NULL REFERENCES users (id),
    kind        notice_kind     NOT NULL,
    data        jsonb           NOT NULL,
        /* jsonb?: varies per kind */
    read        boolean         NOT NULL DEFAULT FALSE,
    tags        text[]          NULL DEFAULT array[]::text[]
);

CREATE TABLE follows (
    id          uuid            PRIMARY KEY DEFAULT uuid_generate_v4(),
    created     timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified    timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id     uuid            NOT NULL REFERENCES users (id),
    entity_id   uuid            NOT NULL, /* ISSUE cant ref across tables */
    entity_kind follow_kind     NOT NULL,
    UNIQUE (user_id, entity_id)
);

CREATE TABLE units_entity_id (
    entity_id   uuid            PRIMARY KEY DEFAULT uuid_generate_v4()
);

CREATE TABLE units (
    version_id  uuid            PRIMARY KEY DEFAULT uuid_generate_v4(),
    created     timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified    timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    entity_id   uuid            NOT NULL REFERENCES units_entity_id (entity_id),
    previous_id uuid            NULL REFERENCES units (version_id),
    language    varchar(5)      NOT NULL DEFAULT 'en'
        CONSTRAINT lang_check CHECK (language ~* '^\w{2}(-\w{2})?$'),
    name        text            NOT NULL,
    status      entity_status   NOT NULL DEFAULT 'pending',
    available   boolean         NOT NULL DEFAULT TRUE,
    tags        text[]          NULL DEFAULT array[]::text[],
    user_id     uuid            NOT NULL REFERENCES users (id),
    /* and the rest.... */
    body        text            NOT NULL,
    require_ids uuid[]          NOT NULL DEFAULT array[]::uuid[]  /* ISSUE no ELEMENT */
);

CREATE TABLE subjects_entity_id (
    entity_id   uuid            PRIMARY KEY DEFAULT uuid_generate_v4()
);

CREATE TABLE subjects (
    version_id  uuid            PRIMARY KEY DEFAULT uuid_generate_v4(),
    created     timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified    timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    entity_id   uuid            NOT NULL REFERENCES subjects_entity_id (entity_id),
    previous_id uuid            NULL REFERENCES subjects (version_id),
    language    varchar(5)      NOT NULL DEFAULT 'en'
        CONSTRAINT lang_check CHECK (language ~* '^\w{2}(-\w{2})?$'),
    name        text            NOT NULL,
    status      entity_status   NOT NULL DEFAULT 'pending',
    available   boolean         NOT NULL DEFAULT TRUE,
    tags        text[]          NULL DEFAULT array[]::text[],
    user_id     uuid            NOT NULL REFERENCES users (id),
    /* and the rest.... */
    body        text            NOT NULL,
    members     jsonb           NOT NULL
        /* jsonb?: ISSUE cant ref, cant enum composite */
);

CREATE TABLE cards_entity_id (
    entity_id   uuid            PRIMARY KEY DEFAULT uuid_generate_v4()
);

CREATE TABLE cards (
    version_id  uuid            PRIMARY KEY DEFAULT uuid_generate_v4(),
    created     timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified    timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    entity_id   uuid            NOT NULL REFERENCES cards_entity_id (entity_id),
    previous_id uuid            NULL REFERENCES cards (version_id),
    language    varchar(5)      NOT NULL DEFAULT 'en'
        CONSTRAINT lang_check CHECK (language ~* '^\w{2}(-\w{2})?$'),
    name        text            NOT NULL,
    status      entity_status   NOT NULL DEFAULT 'pending',
    available   boolean         NOT NULL DEFAULT TRUE,
    tags        text[]          NULL DEFAULT array[]::text[],
    user_id     uuid            NOT NULL REFERENCES users (id),
    /* and the rest.... */
    unit_id     uuid            NOT NULL REFERENCES units_entity_id (entity_id),
    require_ids uuid[]          NOT NULL DEFAULT array[]::uuid[], /* ISSUE no ELEMENT */
    kind        card_kind       NOT NULL,
    data        jsonb           NOT NULL
        /* jsonb?: varies per kind */
);

CREATE TABLE cards_parameters (
    id          uuid            PRIMARY KEY DEFAULT uuid_generate_v4(),
    created     timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified    timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    entity_id   uuid            NOT NULL UNIQUE REFERENCES cards_entity_id (entity_id),
    guess_distribution  jsonb   NOT NULL,
        /* jsonb?: map */
    slip_distribution   jsonb   NOT NULL
);

CREATE TABLE users_subjects (
    id          uuid            PRIMARY KEY DEFAULT uuid_generate_v4(),
    created     timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified    timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id     uuid            NOT NULL REFERENCES users (id),
    subject_id  uuid            NOT NULL REFERENCES subjects_entity_id (entity_id),
    UNIQUE (user_id, subject_id)
);

CREATE TABLE responses (
    id          uuid            PRIMARY KEY DEFAULT uuid_generate_v4(),
    created     timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified    timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id     uuid            NOT NULL REFERENCES users (id),
    card_id     uuid            NOT NULL REFERENCES cards_entity_id (entity_id),
    unit_id     uuid            NOT NULL REFERENCES units_entity_id (entity_id),
    response    text            NOT NULL,
    score       double precision NOT NULL
        CHECK (score >= 0 AND score <= 1),
    learned     double precision NOT NULL
        CHECK (score >= 0 AND score <= 1)
);

CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.modified = now();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_modified
    BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE PROCEDURE update_modified_column();

CREATE TRIGGER update_topics_modified
    BEFORE UPDATE ON topics
    FOR EACH ROW EXECUTE PROCEDURE update_modified_column();

CREATE TRIGGER update_posts_modified
    BEFORE UPDATE ON posts
    FOR EACH ROW EXECUTE PROCEDURE update_modified_column();

CREATE TRIGGER update_notices_modified
    BEFORE UPDATE ON notices
    FOR EACH ROW EXECUTE PROCEDURE update_modified_column();

CREATE TRIGGER update_follows_modified
    BEFORE UPDATE ON follows
    FOR EACH ROW EXECUTE PROCEDURE update_modified_column();

CREATE TRIGGER update_units_modified
    BEFORE UPDATE ON units
    FOR EACH ROW EXECUTE PROCEDURE update_modified_column();

CREATE TRIGGER update_subjects_modified
    BEFORE UPDATE ON subjects
    FOR EACH ROW EXECUTE PROCEDURE update_modified_column();

CREATE TRIGGER update_cards_modified
    BEFORE UPDATE ON cards
    FOR EACH ROW EXECUTE PROCEDURE update_modified_column();

CREATE TRIGGER update_cards_parameters_modified
    BEFORE UPDATE ON cards_parameters
    FOR EACH ROW EXECUTE PROCEDURE update_modified_column();

CREATE TRIGGER update_users_subjects_modified
    BEFORE UPDATE ON users_subjects
    FOR EACH ROW EXECUTE PROCEDURE update_modified_column();

CREATE TRIGGER update_responses_modified
    BEFORE UPDATE ON responses
    FOR EACH ROW EXECUTE PROCEDURE update_modified_column();

/**** SUGGESTS ***************************************************************/

CREATE TABLE suggests (
  id          uuid            PRIMARY KEY DEFAULT uuid_generate_v4(),
  created     timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  modified    timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  name        text            NOT NULL,
  body        text            NOT NULL
);

CREATE TABLE suggests_followers (
  id          uuid            PRIMARY KEY DEFAULT uuid_generate_v4(),
  created     timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  modified    timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  suggest_id  uuid            NOT NULL REFERENCES suggests (id),
  email       text            NULL,
  session_id  uuid            NULL,
  user_id     uuid            NULL,
  CHECK (session_id IS NOT NULL OR user_id IS NOT NULL),
  UNIQUE (suggest_id, session_id),
  UNIQUE (suggest_id, user_id)
);

CREATE TRIGGER update_suggests_modified
    BEFORE UPDATE ON suggests
    FOR EACH ROW EXECUTE PROCEDURE update_modified_column();

CREATE TRIGGER update_suggests_followers_modified
    BEFORE UPDATE ON suggests_followers
    FOR EACH ROW EXECUTE PROCEDURE update_modified_column();

/*

Later: comments, bids, sponsors

suggests_comments
- id, created, modified, suggest_id, user_id, body

suggests_bids
- id, created, modified, suggest_id, user_id, status, data[price, duration, scope, background]

suggests_sponsors
- id, created, modified, bid_id, user_id, price, status, expires_at

*/
