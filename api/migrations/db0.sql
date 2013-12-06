/*
DEFAULT CHAR SET IS UTF-8
POSTGRES v 9.1
*/


DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE users (
    id          varchar(64) PRIMARY KEY,
    created     timestamp DEFAULT current_timestamp,
    modified    timestamp DEFAULT current_timestamp,
    username    varchar(256) UNIQUE,
    email       varchar(256) UNIQUE,
    password    varchar(256),
    ip          inet[],
    role        varchar(64),
    status      varchar(64),
    avatar      varchar(128)
);
GRANT ALL PRIVILEGES ON TABLE users TO sagefy;


DROP TABLE IF EXISTS notifications CASCADE;
CREATE TABLE notifications (
    id                  varchar(64) PRIMARY KEY,
    created             timestamp DEFAULT current_timestamp,
    modified            timestamp DEFAULT current_timestamp,
    notification_type   varchar(64)
    format              varchar(64)
    from_user_id        varchar(64) REFERENCES users(id),
    to_user_id          varchar(64) REFERENCES users(id),
    subject             text,
    body                text,
    read                boolean DEFAULT FALSE
);
GRANT ALL PRIVILEGES ON TABLE notifications TO sagefy;


DROP TABLE IF EXISTS messages CASCADE;
CREATE TABLE messages (
    id              varchar(64) PRIMARY KEY,
    created         timestamp DEFAULT current_timestamp,
    modified        timestamp DEFAULT current_timestamp,
    message_type    varchar(64),
    user_id         varchar(64) REFERENCES users(id),
    object_id       varchar(64),
    object_type     varchar(64),
    subject         text,
    body            text,
    action          varchar(64),
    action_url      varchar(128),
    seen            boolean DEFAULT FALSE

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
