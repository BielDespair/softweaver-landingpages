FROM nginx:alpine

RUN apk add --no-cache python3

COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY cafe/ /usr/share/nginx/html/cafe/
COPY softweaver/ /usr/share/nginx/html/softweaver/

COPY api/questionario_api.py /opt/questionario/api.py
RUN mkdir -p /data \
 && printf '#!/bin/sh\n(while true; do python3 /opt/questionario/api.py; echo "questionario-api caiu, reiniciando..." >&2; sleep 2; done) &\n' \
      > /docker-entrypoint.d/40-questionario-api.sh \
 && chmod +x /docker-entrypoint.d/40-questionario-api.sh