
import os
from pyspark.sql import SparkSession

print("Initializing PySpark Session...")

# Initialize Spark with the required Hadoop-AWS S3 connectors
spark = SparkSession.builder \
    .appName("NativeMinIOConnectionTest") \
    .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.4") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://127.0.0.1:9000") \
    .config("spark.hadoop.fs.s3a.access.key", "admin") \
    .config("spark.hadoop.fs.s3a.secret.key", "supersecretpassword") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false") \
    .getOrCreate()

print("Spark Session established successfully!")

# 1. Create a dummy production log dataset
data = [
    ("User_A", "2026-05-31", "Login", "Success"),
    ("User_B", "2026-05-31", "Purchase", "Failed"),
    ("User_C", "2026-05-31", "Logout", "Success")
]
columns = ["username", "event_date", "action", "status"]

# 2. Build a distributed DataFrame
df = spark.createDataFrame(data, schema=columns)
print("\n--- Current Dataframe View ---")
df.show()

# 3. Write the DataFrame directly into your local 'raw' MinIO bucket
print("Streaming dataframe to local MinIO data lake...")
df.write \
    .mode("overwrite") \
    .parquet("s3a://raw/server_logs")

print("\n🚀 Pipeline Test Complete! Check your MinIO browser dashboard.")
