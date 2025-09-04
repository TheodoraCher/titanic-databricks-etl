#SILVER LAYER - Transformations and write to silver delta table


#Load bronze table
df = spark.table('titanic_bronze')
df.display()

# Import 
from pyspark.sql.types import * 
from pyspark.sql.functions import * 

#Drop duplicates
df=df.dropDuplicates()


# Type casting
df = df.withColumn('survived', col('survived').cast('boolean')).\
        withColumn('age', col('age').cast('integer')).\
        withColumn('fare', round(col('fare').cast('double'), 2))

#Encode categorical: sex
df=df.withColumn('sex',regexp_replace(col('sex'),'female','F')).\
    withColumn('sex',regexp_replace(col('sex'),'male','M'))

# Handle missing values (age → median)
median_age = df.approxQuantile('age', [0.5], 0.0)[0]
df = df.fillna({'age': median_age})

#display
df.display()

# Save as Silver Table
df.write.format("delta").mode("overwrite").option("mergeSchema", "true").saveAsTable("titanic_silver")

