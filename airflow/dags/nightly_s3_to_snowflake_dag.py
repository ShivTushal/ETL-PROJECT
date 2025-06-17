from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import mysql.connector
import boto3
import snowflake.connector
import os

BUCKET_NAME = 'etlprojectinsurance'
S3_FOLDER = 'daily_exports'

def export_mysql_and_upload():
    conn = mysql.connector.connect(
        host='mysql',
        user='root',
        password='root',
        database='insurance_db'
    )
    query = """
        SELECT * FROM insurance_interest
        WHERE DATE(submission_time) = CURDATE() - INTERVAL 1 DAY
    """
    df = pd.read_sql(query, conn)
    conn.close()

    file_date = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
    filename = f"/tmp/insurance_{file_date}.csv"
    df.to_csv(filename, index=False)

    s3_key = f"{S3_FOLDER}/{os.path.basename(filename)}"
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )
    s3.upload_file(filename, BUCKET_NAME, s3_key)
    return s3_key

def load_from_s3_to_snowflake(**context):
    s3_key = context['ti'].xcom_pull(task_ids='export_and_upload')
    s3_path = f"s3://{BUCKET_NAME}/{s3_key}"
    conn = snowflake.connector.connect(
        user=os.getenv('SHIVTUSHAL'),
        password=os.getenv('shiv_tushalSHIV"GOODGOD97"TUSHAL'),
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        warehouse=os.getenv('COMPUTE_WH'),
        database=os.getenv('INSURANCE_DB'),
        schema=os.getenv('PUBLIC'),
        role=os.getenv('ACCOUNTADMIN')
    )
    cursor = conn.cursor()
    cursor.execute(f"""
        COPY INTO insurance_interest
        FROM '{s3_path}'
        FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY = '"')
        ON_ERROR = 'CONTINUE';
    """)
    cursor.close()
    conn.close()

default_args = {
    'owner': 'shiv',
    'start_date': datetime(2025, 6, 15),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='nightly_s3_to_snowflake',
    default_args=default_args,
    schedule_interval='0 0 * * *',
    catchup=False,
    tags=['etl', 's3', 'snowflake']
) as dag:

    export_and_upload = PythonOperator(
        task_id='export_and_upload',
        python_callable=export_mysql_and_upload
    )

    load_to_snowflake = PythonOperator(
        task_id='load_to_snowflake',
        python_callable=load_from_s3_to_snowflake,
        provide_context=True
    )

    export_and_upload >> load_to_snowflake
