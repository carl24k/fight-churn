CREATE TABLE IF NOT EXISTS  x.observation
(
    account_id integer NOT NULL,
    observation_date date NOT NULL,
    is_churn boolean NULL)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE x.observation
    OWNER to postgres;

CREATE INDEX IF NOT EXISTS  observation_date_idx
    ON x.observation USING btree
    (observation_date)
    TABLESPACE pg_default;

CREATE UNIQUE INDEX IF NOT EXISTS  idx_observation_account_date
    ON x.observation USING btree
    (account_id, observation_date)
    TABLESPACE pg_default;
