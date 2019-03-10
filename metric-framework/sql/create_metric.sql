-- Table: x.metric
-- DROP TABLE x.metric;

CREATE TABLE x.metric
(
    account_id integer NOT NULL,
    metric_time timestamp(6) without time zone NOT NULL,
    metric_name_id integer NOT NULL,
    metric_value real
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE x.metric
    OWNER to postgres;

-- Index: idx_metric_account_id

-- DROP INDEX x.idx_metric_account_id;

CREATE INDEX idx_metric_account_id
    ON x.metric USING btree
    (account_id)
    TABLESPACE pg_default;

-- Index: idx_metric_account_time

-- DROP INDEX x.idx_metric_account_time;

CREATE UNIQUE INDEX idx_metric_account_time
    ON x.metric USING btree
    (account_id, metric_name_id, metric_time)
    TABLESPACE pg_default;

-- Index: idx_metric_time

-- DROP INDEX x.idx_metric_time;

CREATE INDEX idx_metric_time
    ON x.metric USING btree
    (metric_time, metric_name_id)
    TABLESPACE pg_default;

-- Index: idx_metric_type

-- DROP INDEX x.idx_metric_type;

CREATE INDEX idx_metric_type
    ON x.metric USING btree
    (metric_name_id)
    TABLESPACE pg_default;