CREATE TABLE IF NOT EXISTS  livebook.event
(
    account_id character(32),
    event_time timestamp(6) without time zone NOT NULL,
    event_type text COLLATE pg_catalog."default",
    product_id integer,
    additional_data text COLLATE pg_catalog."default"
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE livebook.event
    OWNER to postgres;

CREATE INDEX  IF NOT EXISTS  idx_event_account_id
    ON livebook.event USING btree
    (account_id)
    TABLESPACE pg_default;

CREATE INDEX  IF NOT EXISTS  idx_event_account_time
    ON livebook.event USING btree
    (account_id, event_time)
    TABLESPACE pg_default;

CREATE INDEX  IF NOT EXISTS  idx_event_time
    ON livebook.event USING btree
    (event_time)
    TABLESPACE pg_default;

CREATE INDEX  IF NOT EXISTS  idx_event_type
    ON livebook.event USING btree
    (event_type)
    TABLESPACE pg_default;

CREATE INDEX  IF NOT EXISTS  idx_product_id
    ON livebook.event USING btree
    (product_id)
    TABLESPACE pg_default;
