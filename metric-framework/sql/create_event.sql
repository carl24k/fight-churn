-- Table: x.event

-- DROP TABLE x.event;

CREATE TABLE x.event
(
    account_id integer NOT NULL,
    event_time timestamp(6) without time zone NOT NULL,
    event_type_id integer NOT NULL
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE x.event
    OWNER to postgres;

-- Index: idx_event_account_id

-- DROP INDEX x.idx_event_account_id;

CREATE INDEX idx_event_account_id
    ON x.event USING btree
    (account_id)
    TABLESPACE pg_default;

-- Index: idx_event_account_time

-- DROP INDEX x.idx_event_account_time;

CREATE INDEX idx_event_account_time
    ON x.event USING btree
    (account_id, event_time)
    TABLESPACE pg_default;

-- Index: idx_event_time

-- DROP INDEX x.idx_event_time;

CREATE INDEX idx_event_time
    ON x.event USING btree
    (event_time)
    TABLESPACE pg_default;

-- Index: idx_event_type

-- DROP INDEX x.idx_event_type;

CREATE INDEX idx_event_type
    ON x.event USING btree
    (event_type_id)
    TABLESPACE pg_default;
