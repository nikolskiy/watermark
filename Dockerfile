FROM python:3.7-alpine

RUN apk add --no-cache \
    jpeg-dev \
    zlib-dev \
    freetype-dev \
    lcms2-dev \
    openjpeg-dev \
    tiff-dev \
    tcl-dev \
    build-base \
    bash \
    linux-headers && \
    pip3 install --upgrade pip

# Make sure we don't reload Pillow if requirements change
RUN pip3 install Pillow==6.0.0

# At this point heavy lifting is done and everything below will build fast.


# Copy python requirements file
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

# Remove pip cache. We are not going to need it anymore
RUN rm -r /root/.cache

# Add our application files
RUN mkdir /tmp/watermark
RUN mkdir app
COPY ./app /app
WORKDIR /app

ENV PYTHONUNBUFFERED 1
EXPOSE 8080

CMD ["python3", "main.py"]

