from pyspark.sql import SparkSession
import os
from pyspark.sql.functions import concat_ws , struct , to_json, col
from pymongo.mongo_client import MongoClient
from elasticsearch import Elasticsearch


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
#df.write.mode('overwrite').csv('/home/cong/Downloads/data.csv' , header = True)
#df.coalesce(1).write.mode('overwrite').csv('/home/cong/Downloads/data.csv' , header = True)
# tang kich thuoc partitions
#df.repartition(10)

es = Elasticsearch([{'host': 'loacalhost', 'port': 9200}])

def write_to_elasticsearch(rows):
	index_id = 0
	for row in rows:
		res = es.index(index='my_index', id=index_id, body=row.asDict())
		print(f'insert thanh cong')
		index_id +=1
		
df.foreachPartition(write_to_elasticsearch)
