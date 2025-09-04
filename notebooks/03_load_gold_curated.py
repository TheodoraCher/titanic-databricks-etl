#GOLD LAYER- Curated data and load to gold delta table

#Load silver table
df = spark.table('titanic_silver')
df.display()

# Import 
from pyspark.sql.types import * 
from pyspark.sql.functions import * 

# Feature: has_cabin 
df=df.withColumn('has_cabin', when(col('cabin').isNotNull(),1 ).otherwise(0))

# Feature: title (from name)
df = df.withColumn('title', regexp_extract(col('name'), r'(Mr|Mrs|Miss|Master|Mis)', 1))
df=df.withColumn('title', when(col('title')=='','Other').otherwise(col('title')))

# Feature: family_size (sibsp + parch + self)
df = df.withColumn("family_size", col("sibsp") + col("parch") + lit(1))

# Feature: age_group
df = df.withColumn(
    "age_group",
    when(col("age") < 13, "Child")
    .when((col("age") >= 13) & (col("age") < 18), "Teen")
    .when((col("age") >= 18) & (col("age") < 60), "Adult")
    .otherwise("Senior")
)

# Drop useless columns
df = df.drop("ticket", "body", "boat", "home.dest", "name", "cabin")

# Load to gold delta table
df.write.format('delta').mode('overwrite').option("mergeSchema", "true").saveAsTable("titanic_gold")
