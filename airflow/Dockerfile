FROM apache/airflow:2.8.1-python3.10
USER root
RUN apt-get update && apt-get install -y curl unzip
USER airflow
COPY dags /opt/airflow/dags
RUN pip install pandas boto3 mysql-connector-python snowflake-connector-python
