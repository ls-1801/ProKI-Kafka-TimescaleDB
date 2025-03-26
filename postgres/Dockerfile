FROM timescale/timescaledb:latest-pg15

COPY flatten.sh /flatten.sh
RUN chmod +x /flatten.sh
COPY tables /tables
RUN /flatten.sh && ls /docker-entrypoint-initdb.d/
