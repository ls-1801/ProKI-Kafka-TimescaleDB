CREATE SCHEMA chair2;
CREATE USER grafana_chair2 WITH PASSWORD 'grafana';
GRANT USAGE ON SCHEMA chair2 TO grafana_chair2;
ALTER ROLE grafana_chair2 SET search_path = 'chair2';