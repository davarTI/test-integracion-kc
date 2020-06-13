FROM williamyeh/behave

COPY ./features /behave/features
COPY wrapper.sh /tmp/wrapper.sh
