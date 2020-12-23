CREATE TABLE IF NOT EXISTS  livebook.metric
(
    account_id character(32),
    metric_time timestamp(6) without time zone NOT NULL,
    metric_name_id integer NOT NULL,
    metric_value real
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE livebook.metric
    OWNER to postgres;


CREATE INDEX IF NOT EXISTS  idx_metric_account_id
    ON livebook.metric USING btree
    (account_id)
    TABLESPACE pg_default;


CREATE UNIQUE INDEX IF NOT EXISTS  idx_metric_account_time
    ON livebook.metric USING btree
    (account_id, metric_name_id, metric_time)
    TABLESPACE pg_default;


CREATE INDEX IF NOT EXISTS  idx_metric_time
    ON livebook.metric USING btree
    (metric_time, metric_name_id)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS  idx_metric_type
    ON livebook.metric USING btree
    (metric_name_id)
    TABLESPACE pg_default;
