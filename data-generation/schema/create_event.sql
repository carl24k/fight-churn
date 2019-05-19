CREATE TABLE IF NOT EXISTS  x.event
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

CREATE INDEX  IF NOT EXISTS  idx_event_account_id
    ON x.event USING btree
    (account_id)
    TABLESPACE pg_default;

CREATE INDEX  IF NOT EXISTS  idx_event_account_time
    ON x.event USING btree
    (account_id, event_time)
    TABLESPACE pg_default;

CREATE INDEX  IF NOT EXISTS  idx_event_time
    ON x.event USING btree
    (event_time)
    TABLESPACE pg_default;

CREATE INDEX  IF NOT EXISTS  idx_event_type
    ON x.event USING btree
    (event_type_id)
    TABLESPACE pg_default;
