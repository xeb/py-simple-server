FROM gliderlabs/registrator:latest
COPY start.sh /start.sh
RUN apk-install -t curl
ENTRYPOINT [ "./start.sh" ]
