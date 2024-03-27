FROM wurstmeister/kafka:2.13-2.8.1

WORKDIR /scritps
COPY * .
RUN rm entrypoint.sh
COPY entrypoint.sh /

ENTRYPOINT ["/entrypoint.sh"]
