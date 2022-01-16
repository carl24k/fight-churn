CREATE TABLE IF NOT EXISTS  liveproject.metric_name
(
    metric_name_id integer NOT NULL,
    metric_name text COLLATE pg_catalog."default"
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE liveproject.metric_name
    OWNER to postgres;


CREATE UNIQUE INDEX IF NOT EXISTS  idx_metric_name_id
    ON liveproject.metric_name USING btree
    (metric_name_id)
    TABLESPACE pg_default;

CREATE UNIQUE INDEX IF NOT EXISTS  idx_metric_name_name
    ON liveproject.metric_name USING btree
    (metric_name)
    TABLESPACE pg_default;
