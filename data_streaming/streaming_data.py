from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, FloatType


kafka_schema = StructType(
    [
        StructField("ECG_data", FloatType())
    ]
)

spark = SparkSession.builder\
    .appName("ESP32 Streaming Data") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

# Lee datos desde Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "esp32/data") \
    .load()

print(df)