FROM apache/airflow:2.9.2-python3.11
ENV PATH="/home/airflow/.local/bin:${PATH}"
ENV LD_LIBRARY_PATH=/opt/oracle/instantclient_2_11
USER root
RUN apt-get update && apt-get install -y libaio1 unzip && apt-get clean && rm -rf /var/lib/apt/lists/*
ADD https://download.oracle.com/otn_software/linux/instantclient/2114000/instantclient-basic-linux.x64-21.14.0.0.0dbru.zip /tmp/
RUN unzip /tmp/instantclient-basic-linux.x64-21.14.0.0.0dbru.zip -d /opt/oracle && \
    rm /tmp/instantclient-basic-linux.x64-21.14.0.0.0dbru.zip
USER airflow
COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.9.2/constraints-3.11.txt"