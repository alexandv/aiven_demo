# vim: set filetype=dockerfile:

# We use the builder image to compile some modules that use gcc.
# psycopg2 has an alpine package which makes it eaiser to install
FROM python:3.6.2-alpine3.6 as builder

RUN apk add --update postgresql-dev gcc musl-dev libxslt-dev

COPY pip/requirements.txt .
RUN pip install -r requirements.txt

FROM python:3.6.2-alpine3.6

RUN apk add --update libpq libxslt libxml2

RUN rm -rf /usr/local/lib/python3.6/site-packages/
COPY --from=builder /usr/local/lib/python3.6/site-packages/ /usr/local/lib/python3.6/site-packages/

# This will create the group wato and the home directory with proper permissions
RUN adduser -h /aiven -D aiven

COPY aiven /aiven/
RUN chown -R aiven:aiven /aiven && chmod -R 700 /aiven

USER aiven
WORKDIR /aiven
ENV PYTHONPATH /aiven

# The default command which can be replaced is to display usage
CMD ["--help"]

ENTRYPOINT ["python","aiven/aiven_cmd.py"]
