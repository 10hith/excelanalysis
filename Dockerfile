FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

USER root

# Install Java
ARG openjdk_version="11"

RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends \
    "openjdk-${openjdk_version}-jre-headless" \
    ca-certificates-java && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Spark Installation
WORKDIR /tmp
RUN wget https://archive.apache.org/dist/spark/spark-3.1.2/spark-3.1.2-bin-hadoop3.2.tgz && \
    tar xzf spark-3.1.2-bin-hadoop3.2.tgz -C /opt && \
    rm spark-3.1.2-bin-hadoop3.2.tgz

ENV SPARK_HOME=/opt/spark-3.1.2-bin-hadoop3.2

# Configure Spark
ENV SPARK_OPTS="--driver-java-options=-Xms1024M --driver-java-options=-Xmx4096M --driver-java-options=-Dlog4j.logLevel=info" \
    PATH="${PATH}:${SPARK_HOME}/bin"

# Copy project files
COPY ./app /app/
COPY . .
ENV PYTHONPATH "${PYTHONPATH}:/excelanalysis"