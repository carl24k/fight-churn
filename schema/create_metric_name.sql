-- Table: x.metric_name

-- DROP TABLE x.metric_name;

CREATE TABLE x.metric_name
(
    metric_name_id integer NOT NULL,
    metric_name_name text COLLATE pg_catalog."default"
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE x.metric_name
    OWNER to postgres;
