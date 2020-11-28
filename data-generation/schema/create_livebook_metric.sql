-- Table: livebook.metric

-- DROP TABLE livebook.metric;

CREATE TABLE livebook.metric
(
    account_id character(32) COLLATE pg_catalog."default",
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

 Index: idx_metric_account_id

 DROP INDEX livebook.idx_metric_account_id;

CREATE INDEX idx_metric_account_id
    ON livebook.metric USING btree
    (account_id COLLATE pg_catalog."default")
    TABLESPACE pg_default;

 Index: idx_metric_account_time

 DROP INDEX livebook.idx_metric_account_time;

CREATE UNIQUE INDEX idx_metric_account_time
    ON livebook.metric USING btree
    (account_id COLLATE pg_catalog."default", metric_name_id, metric_time)
    TABLESPACE pg_default;

 Index: idx_metric_time

 DROP INDEX livebook.idx_metric_time;

CREATE INDEX idx_metric_time
    ON livebook.metric USING btree
    (metric_time, metric_name_id)
    TABLESPACE pg_default;

 Index: idx_metric_type

 DROP INDEX livebook.idx_metric_type;

CREATE INDEX idx_metric_type
    ON livebook.metric USING btree
    (metric_name_id)
    TABLESPACE pg_default;
    