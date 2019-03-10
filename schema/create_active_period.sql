-- Table: x.active_period

-- DROP TABLE x.active_period;

CREATE TABLE x.active_period
(
    account_id integer NOT NULL,
    start_date date NOT NULL,
    churn_date date NULL
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE x.active_period
    OWNER to postgres;

-- Index: start_date_idx

-- DROP INDEX x.start_date_idx;

CREATE INDEX start_date_idx
    ON x.active_period USING btree
    (start_date)
    TABLESPACE pg_default;

CREATE UNIQUE INDEX idx_active_period_account_date
    ON x.active_period USING btree
    (account_id, start_date)
    TABLESPACE pg_default;
