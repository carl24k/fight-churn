# To create connection in Big Query:
# On Query Tab, at the top "ADD DATA" button -> "External Data Source"
# Get the Connection ID (path) from the Connection Info and replace the path in the EXTERNAL_QUERY

DROP TABLE IF EXISTS socialnet7.account;

CREATE TABLE socialnet7.account AS
SELECT *
FROM
   EXTERNAL_QUERY(
     "projects/___/locations/___/connections/___",
      "Select * from socialnet7.account");

DROP TABLE IF EXISTS socialnet7.subscription;

CREATE TABLE
socialnet7.subscription
AS
SELECT
*
FROM
   EXTERNAL_QUERY(
     "projects/___/locations/___/connections/___",
      "Select * from socialnet7.subscription");

DROP TABLE IF EXISTS socialnet7.event;

CREATE TABLE
socialnet7.event
AS
SELECT
*
FROM
   EXTERNAL_QUERY(
     "projects/___/locations/___/connections/___",
      "Select * from socialnet7.event");

DROP TABLE IF EXISTS socialnet7.event_type;


CREATE TABLE
socialnet7.event_type
AS
SELECT
*
FROM
   EXTERNAL_QUERY(
     "projects/___/locations/___/connections/___",
      "Select * from socialnet7.event_type");

