CREATE SCHEMA chair1;
CREATE USER grafana_chair1 WITH PASSWORD 'grafana';
GRANT USAGE ON SCHEMA chair1 TO grafana_chair1;
ALTER ROLE grafana_chair1 SET search_path = 'chair1';