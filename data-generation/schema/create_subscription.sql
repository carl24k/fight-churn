CREATE TABLE IF NOT EXISTS  x.subscription
(
    id integer NOT NULL,
    account_id integer NOT NULL,
    product text COLLATE pg_catalog."default" NOT NULL,
    start_date date NOT NULL,
    end_date date,
    mrr double precision NOT NULL,
    quantity double precision NULL,
    units  text COLLATE pg_catalog."default" NULL,
    bill_period_months integer NOT NULL,
    CONSTRAINT subscription_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE x.subscription
    OWNER to postgres;

CREATE INDEX  IF NOT EXISTS  subscription_date_idx
    ON x.subscription USING btree
    (start_date, end_date)
    TABLESPACE pg_default;

CREATE INDEX  IF NOT EXISTS  subscription_start_idx
    ON x.subscription USING btree
    (start_date)
    TABLESPACE pg_default;
