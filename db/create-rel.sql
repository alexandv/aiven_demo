--------- DROPS

DROP TABLE IF EXISTS event_type;
DROP TABLE IF EXISTS event;

--------- TABLES

CREATE TABLE event_type (
    id          int PRIMARY KEY,
    name        varchar(100) UNIQUE
);

CREATE TABLE event (
    id          int PRIMARY KEY,
    event_type_id int REFERENCES event_type,
    description varchar(200)
);

--------- INSERTS

INSERT INTO event_type(id,name) VALUES (1,'aiven');
