/*
    This is a part of a proposed changed back to PostgreSQL from RethinkDB.
    This schema is still evolving.
    No decision has been made.
*/

/* set to UTF-8 */

/* TODO default values ? */

CREATE TABLE users (
    id          char(24)        PRIMARY KEY,
    created     timestamp       NOT NULL,  /* TODO auto on create? */
    modified    timestamp       NOT NULL,  /*  TODO auto on modify? */
    name        text            UNIQUE,
    email       text            UNIQUE,
    password    varchar(60)     NOT NULL,   /* TODO minlength 8 */
    settings    json            NOT NULL,
);

CREATE TABLE users_sets (
    id          char(24)        PRIMARY KEY,
    created     timestamp       NOT NULL,  /* TODO auto on create? */
    modified    timestamp       NOT NULL,  /* TODO auto on modify? */
    user_id     char(24)        UNIQUE,  /* TODO foreign key? */
    set_ids     char(24)[],     /* TODO foreign key? TODO migrate to entry per relation? */
);

CREATE TABLE topics (
    id          char(24)        PRIMARY KEY,
    created     timestamp       NOT NULL,  /* TODO auto on create? */
    modified    timestamp       NOT NULL,  /* TODO auto on modify? */
    user_id     char(24)        NOT NULL,  /* TODO foreign key? */
    name        text            NOT NULL,
    entity_id   char(24)        NOT NULL,
    entity_kind enum('card', 'unit', 'set')     NOT NULL,
);

CREATE TABLE posts (
    id          char(24)        PRIMARY KEY,
    created     timestamp       NOT NULL,  /* TODO auto on create? */
    modified    timestamp       NOT NULL,  /* TODO auto on modify? */
    user_id     char(24)        NOT NULL,  /* TODO foreign key? */
    topic_id    char(24)        NOT NULL,  /* TODO foreign key? */
    body        text            NOT NULL,  /* TODO optional when 'vote' */
    kind        enum('post', 'proposal', 'vote')    NOT NULL,
    replies_to_id   char(24)    /* TODO OPTIONAL but required when vote */,
    entity_versions /* TODO array of entity_version_id, entity_kind ONLY WHEN PROPOSAL */,
    /* TODO eliminate name when 'proposal' */
    response    boolean     /* TODO only required when 'vote' */,
);

CREATE TABLE notices (
    id          char(24)        PRIMARY KEY,
    created     timestamp       NOT NULL,  /* TODO auto on create? */
    modified    timestamp       NOT NULL,  /* TODO auto on modify? */
    user_id     char(24)        NOT NULL,  /* TODO foreign key? */
    kind        enum('create_topic', 'create_proposal', 'block_proposal', 'decline_proposal', 'accept_proposal', 'create_post', 'come_back')  NOT NULL,
    data        json            NOT NULL,
    read        boolean         NOT NULL,
    tags        text[]          /* TODO optional */,
);

CREATE TABLE follows (
    id          char(24)        PRIMARY KEY,
    created     timestamp       NOT NULL,  /* TODO auto on create? */
    modified    timestamp       NOT NULL,  /* TODO auto on modify? */
    user_id     char(24)        NOT NULL,  /* TODO foreign key? */
    entity_id   char(24)        NOT NULL,  /* TODO foreign key? */
    entity_kind enum('card', 'unit', 'set', 'topic') NOT NULL,
);

CREATE TABLE units (
    version_id  char(24)        PRIMARY KEY,
    created     timestamp       NOT NULL,  /* TODO auto on create? */
    modified    timestamp       NOT NULL,  /* TODO auto on modify? */
    entity_id   char(24)        NOT NULL,
    previous_id char(24)        /* TODO optional */, /* TODO verify-able ? */
    language    varchar(5)      NOT NULL,
    name        text            NOT NULL,
    status      enum('pending', 'blocked', 'declined', 'accepted')  NOT NULL,
    available   boolean         NOT NULL,
    tags        text[]          /* TODO optional */,
    /* and the rest.... */
    body        text            NOT NULL,
    require_ids varchar(24)[]   NOT NULL,  /* TODO foreign key? */
);

CREATE TABLE sets (
    /* TODO unit starters plus... */
    body        text            NOT NULL,
    members /* TODO array of entity_id (foreign?), entity_kind enum(unit, set)... required */,
);

CREATE TABLE cards (
    /* TODO unit starters plus... */
    unit_id     char(24)     NOT NULL, /* TODO foreign key? */
    require_ids char(24)[]   NOT NULL, /* TODO foriegn key? */
    kind    enum('video', 'choice')  NOT NULL,
    data        json            NOT NULL, /* TODO custom fields per kind */
);

CREATE TABLE cards_parameters (
    id          char(24)        PRIMARY KEY,
    created     timestamp       NOT NULL,  /* TODO auto on create? */
    modified    timestamp       NOT NULL,  /* TODO auto on modify? */
    entity_id   char(24)        UNIQUE,   /* TODO  foriegn key? */
    guess_distribution  json    NOT NULL,
    slip_distribution   json    NOT NULL,
);

CREATE TABLE responses (
    id          char(24)        PRIMARY KEY,
    created     timestamp       NOT NULL,  /* TODO auto on create? */
    modified    timestamp       NOT NULL,  /* TODO auto on modify? */
    user_id     char(24)        NOT NULL, /* TODO foriegn key? */
    card_id     char(24)        NOT NULL, /* TODO foreign key? */
    unit_id     char(24)        NOT NULL, /* TODO foreign key? */
    response    text            NOT NULL,
    score       float           NOT NULL, /* TODO must be 0->1 */
    learned     float           NOT NULL, /* TODO must be 0->1 */
);
