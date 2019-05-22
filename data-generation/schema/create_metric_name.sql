CREATE TABLE IF NOT EXISTS  x.metric_name
(
    metric_name_id integer NOT NULL,
    metric_name text COLLATE pg_catalog."default"
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE x.metric_name
    OWNER to postgres;


CREATE UNIQUE INDEX IF NOT EXISTS  idx_metric_name_id
    ON x.metric_name USING btree
    (metric_name_id)
    TABLESPACE pg_default;

CREATE UNIQUE INDEX IF NOT EXISTS  idx_metric_name_name
    ON x.metric_name USING btree
    (metric_name)
    TABLESPACE pg_default;
