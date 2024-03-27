CREATE SCHEMA chair1;
CREATE USER grafana_chair1 WITH PASSWORD 'grafana';
GRANT USAGE ON SCHEMA chair1 TO grafana_chair1;
ALTER ROLE grafana_chair1 SET search_path = 'chair1';

-- We start by creating a regular SQL table
CREATE TABLE chair1.bigmachine (
  time        	TIMESTAMP(6)    NOT NULL,
  x   		BIGINT          NOT NULL,
  y 		BIGINT          NOT NULL,
  z    		BIGINT  	NOT NULL
);
GRANT SELECT ON chair1.bigmachine TO grafana_chair1;

-- Then we convert it into a hypertable that is partitioned by time
SELECT create_hypertable('chair1.bigmachine', 'time');
