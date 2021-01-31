-- Table: livebook.observation
CREATE TABLE livebook.observation
(
    account_id character(32) COLLATE pg_catalog."default" NOT NULL,
    observation_date date NOT NULL,
    is_churn boolean
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE livebook.observation
    OWNER to postgres;

-- Index: idx_observation_account_date

CREATE UNIQUE INDEX idx_observation_account_date
    ON livebook.observation USING btree
    (account_id COLLATE pg_catalog."default", observation_date)
    TABLESPACE pg_default;

-- Index: observation_date_idx

CREATE INDEX observation_date_idx
    ON livebook.observation USING btree
    (observation_date)
    TABLESPACE pg_default;
