ARG ELK_VERSION
FROM logstash:${ELK_VERSION}
RUN logstash-plugin install logstash-input-http logstash-filter-aggregate \
    logstash-filter-prune logstash-output-email

COPY logstash.conf   /usr/share/logstash/pipeline/
EXPOSE 5000
