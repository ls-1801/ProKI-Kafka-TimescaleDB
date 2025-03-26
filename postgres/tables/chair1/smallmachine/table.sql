-- We start by creating a regular SQL table
CREATE TABLE chair1.smallmachine (
  time        	TIMESTAMP(6)    NOT NULL,
  x   		      BIGINT          NOT NULL,
  y 		        BIGINT          NOT NULL
);
GRANT SELECT ON chair1.smallmachine TO grafana_chair1;

-- Then we convert it into a hypertable that is partitioned by time
SELECT create_hypertable('chair1.smallmachine', 'time');
