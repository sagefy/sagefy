/*
DEFAULT CHAR SET IS UTF-8
POSTGRES v 9.1
TODO: Move to Alembic
*/

CREATE USER sagefy password 'sagefy' SUPERUSER;
CREATE DATABASE sagefy;

\connect sagefy;

CREATE TABLE users (
    id          varchar(64) PRIMARY KEY,
    created     timestamp DEFAULT current_timestamp,
    modified    timestamp DEFAULT current_timestamp,
    username    varchar(256) UNIQUE,
    email       varchar(256) UNIQUE,
    password    varchar(256),
    ip          inet[],
    status      varchar(64),
    avatar      varchar(128)
);

GRANT ALL PRIVILEGES ON TABLE users TO sagefy;


CREATE TABLE notifications (
    id                  varchar(64) PRIMARY KEY,
    created             timestamp DEFAULT current_timestamp,
    modified            timestamp DEFAULT current_timestamp,
    subject             text,
    body                text,
    read                boolean DEFAULT FALSE,
    user_id             varchar(64) REFERENCES users(id),
    notification_type   varchar(64)
);

GRANT ALL PRIVILEGES ON TABLE notifications TO sagefy;


CREATE TABLE messages (
    id              varchar(64) PRIMARY KEY,
    created         timestamp DEFAULT current_timestamp,
    modified        timestamp DEFAULT current_timestamp,
    subject         text,
    body            text,
    read            boolean DEFAULT FALSE,
    user_id         varchar(64) REFERENCES users(id),
    message_type    varchar(64)
);

GRANT ALL PRIVILEGES ON TABLE messages TO sagefy;


DROP FUNCTION IF EXISTS update_modified_column() CASCADE;
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
   NEW.modified = now();
   RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_modified BEFORE UPDATE
    ON users FOR EACH ROW EXECUTE PROCEDURE
    update_modified_column();

CREATE TRIGGER update_messages_modified BEFORE UPDATE
    ON messages FOR EACH ROW EXECUTE PROCEDURE
    update_modified_column();

CREATE TRIGGER update_notifications_modified BEFORE UPDATE
    ON notifications FOR EACH ROW EXECUTE PROCEDURE
    update_modified_column();
