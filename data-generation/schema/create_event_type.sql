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


