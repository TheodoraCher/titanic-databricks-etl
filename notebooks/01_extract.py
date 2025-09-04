# BRONZE LAYER - Raw ingest of Titanic CSV into Delta table

# Read Titanic CSV
df = spark.read.format('csv').option('inferSchema',True).option('header',True).load('/Volumes/workspace/first_data/first_volume/titanic.csv')

# Write to Bronze Delta table
df.write.format('delta').mode('overwrite').saveAsTable('titanic_bronze')
