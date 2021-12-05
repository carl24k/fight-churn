CREATE TABLE IF NOT EXISTS  liveproject.event
(
    account_id text COLLATE pg_catalog."default" NOT NULL,
    event_time timestamp(6) without time zone NOT NULL,
    event_type text COLLATE pg_catalog."default" NOT NULL,
    product_id integer,
    additional_data text COLLATE pg_catalog."default"
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE liveproject.event
    OWNER to postgres;

CREATE INDEX  IF NOT EXISTS  idx_event_account_id
    ON liveproject.event USING btree
    (account_id)
    TABLESPACE pg_default;

CREATE INDEX  IF NOT EXISTS  idx_event_account_time
    ON liveproject.event USING btree
    (account_id, event_time)
    TABLESPACE pg_default;

CREATE INDEX  IF NOT EXISTS  idx_event_time
    ON liveproject.event USING btree
    (event_time)
    TABLESPACE pg_default;

CREATE INDEX  IF NOT EXISTS  idx_event_type
    ON liveproject.event USING btree
    (event_type)
    TABLESPACE pg_default;
