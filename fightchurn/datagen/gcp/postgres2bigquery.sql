# To create connection in Big Query:
# On Query Tab, at the top "ADD DATA" button -> "External Data Source"
# Get the Connection ID (path) from the Connection Info

DROP TABLE IF EXISTS socialnet7.account;

CREATE TABLE socialnet7.account AS
SELECT *
FROM
   EXTERNAL_QUERY(
     "projects/.../locations/us-west1/connections/...",
      "Select * from socialnet7.account");

DROP TABLE IF EXISTS socialnet7.subscription;

CREATE TABLE
socialnet7.subscription
AS
SELECT
*
FROM
   EXTERNAL_QUERY(
     "projects/churn-1-352914/locations/us-west1/connections/churn_1",
      "Select * from socialnet7.subscription");

DROP TABLE IF EXISTS socialnet7.event;

CREATE TABLE
socialnet7.event
AS
SELECT
*
FROM
   EXTERNAL_QUERY(
     "projects/churn-1-352914/locations/us-west1/connections/churn_1",
      "Select * from socialnet7.event");

DROP TABLE IF EXISTS socialnet7.event_type;


CREATE TABLE
socialnet7.event_type
AS
SELECT
*
FROM
   EXTERNAL_QUERY(
     "projects/churn-1-352914/locations/us-west1/connections/churn_1",
      "Select * from socialnet7.event_type");

