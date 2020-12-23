CREATE TABLE IF NOT EXISTS  livebook.metric_name
(
    metric_name_id integer NOT NULL,
    metric_name text COLLATE pg_catalog."default"
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE livebook.metric_name
    OWNER to postgres;


CREATE UNIQUE INDEX IF NOT EXISTS  idx_metric_name_id
    ON livebook.metric_name USING btree
    (metric_name_id)
    TABLESPACE pg_default;

CREATE UNIQUE INDEX IF NOT EXISTS  idx_metric_name_name
    ON livebook.metric_name USING btree
    (metric_name)
    TABLESPACE pg_default;
