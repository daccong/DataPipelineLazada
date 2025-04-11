from pyspark.sql import SparkSession
import os
from pyspark.sql.functions import concat_ws , struct , to_json, col
from pymongo.mongo_client import MongoClient
spark = SparkSession.builder\
        .appName('read_data_hdfs')\
        .getOrCreate()
        
hdfs_path = 'hdfs://127.0.0.1:9000/user/cong/noi_luu_file_hdfs/'
df = spark.read.option('multiLine' , True).json(hdfs_path)
#categories
df = df.withColumn('categories' , concat_ws(',' , df['categories']))
# icon
df  = df.withColumn('icons',concat_ws(',' , col('icons.domClass'), col('icons.group'), col('icons.text'), col('icons.showType') , col('icons.type')))
# recommendTips
df = df.withColumn('recommendTips' , to_json(struct('recommendTips.*')))
#skus
df = df.withColumn('skus' , to_json(col('skus.id')))
df = df.withColumn('skus' , concat_ws(',' , col('skus')))
#thumbs
df = df.withColumn('thumbs' , to_json(col('thumbs')))
# luu file 
df.write.mode('overwrite').csv('/home/cong/Downloads/data.csv' , header = True)
#df.coalesce(1).write.mode('overwrite').csv('/home/cong/Downloads/data.csv' , header = True)
# tang kich thuoc partitions
#df.repartition(10)



def get_mongo_collection():
    uri = "mongodb+srv://phandaccong:3103@tiktokcommnet.6ep1ywo.mongodb.net/?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true&appName=tiktokcomment"
    client = MongoClient(uri)
    return client['tiktokcomment']['data_lazada']
def write_to_mongo(rows):
    collection = get_mongo_collection()
    batch = [row.asDict() for row in rows]
    if batch:
        try:
            collection.insert_many(batch)
            print('insert ok')
        except Exception as e:
            print('Error')
df.foreachPartition(write_to_mongo)
