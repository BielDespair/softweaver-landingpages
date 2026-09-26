FROM nginx:alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY cafe/ /usr/share/nginx/html/cafe/
COPY softweaver/ /usr/share/nginx/html/softweaver/

RUN mkdir -p /usr/share/nginx/html/softweaver/questionario/respostas \
 && chown nginx:nginx /usr/share/nginx/html/softweaver/questionario/respostas