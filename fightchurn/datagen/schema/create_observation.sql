CREATE TABLE IF NOT EXISTS  liveproject.observation
(
    account_id text COLLATE pg_catalog."default" NOT NULL,
    observation_date date NOT NULL,
    is_churn boolean NULL)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE liveproject.observation
    OWNER to postgres;

CREATE INDEX IF NOT EXISTS  observation_date_idx
    ON liveproject.observation USING btree
    (observation_date)
    TABLESPACE pg_default;

CREATE UNIQUE INDEX IF NOT EXISTS  idx_observation_account_date
    ON liveproject.observation USING btree
    (account_id, observation_date)
    TABLESPACE pg_default;
