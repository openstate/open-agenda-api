FROM python:2.7-alpine

WORKDIR /opt/oaa/ocd_frontend
COPY requirements.txt /opt/oaa/ocd_frontend/requirements.txt

# Install build base for alpine including gcc for Pillow
RUN apk add --update build-base python-dev py-pip jpeg-dev zlib-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del build-base python-dev py-pip

COPY . /opt/ori/ocd_frontend

CMD python wsgi.py
