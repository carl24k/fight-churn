CREATE TABLE IF NOT EXISTS  x.active_week
(
    account_id integer NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE x.active_week
    OWNER to postgres;


CREATE INDEX IF NOT EXISTS  start_date_idx
    ON x.active_week USING btree
    (start_date)
    TABLESPACE pg_default;

CREATE UNIQUE INDEX IF NOT EXISTS  idx_active_week_account_date
    ON x.active_week USING btree
    (account_id, start_date)
    TABLESPACE pg_default;

