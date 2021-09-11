CREATE TABLE IF NOT EXISTS x.event_type
(
    event_type_id integer NOT NULL,
    event_type_name text COLLATE pg_catalog."default"
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE x.event_type
    OWNER to postgres;



CREATE UNIQUE INDEX IF NOT EXISTS  idx_event_type_id
    ON x.event_type USING btree
    (event_type_id)
    TABLESPACE pg_default;

CREATE UNIQUE INDEX IF NOT EXISTS  idx_event_type_name
    ON x.event_type USING btree
    (event_type_name)
    TABLESPACE pg_default;
