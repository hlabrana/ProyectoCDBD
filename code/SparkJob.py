
# Instalando Dependencias
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode,split,col
from sparkmeasure import StageMetrics

spark = SparkSession.builder.getOrCreate()
stagemetrics = StageMetrics(spark)

PATH = './data/RC_2013-01'

stagemetrics.begin()
df = spark.read.json(PATH)

df.printSchema()
df.count()

comments = df.select(df.body)
comments.show()

SplitData = comments.withColumn('body',explode(split("body"," ")))

frequentWords = SplitData.groupby('body').count().orderBy(col('count').desc())
frequentWords.show()
frequentWords.count()

frequentWords = frequentWords.filter(frequentWords.body != "")
frequentWords.show()
frequentWords.count()

Top15 = spark.createDataFrame(frequentWords.take(15)).toPandas()
Top15

stagemetrics.end()
stagemetrics.print_report()

# Generar gráfica
import matplotlib.pyplot as plt

plt.plot(Top15['body'],Top15['count'],color='red')
plt.bar(Top15['body'],Top15['count'],color='cyan')
plt.xlabel('Top 10 Most Frequent Words')
plt.ylabel('Absolute Frequency')
plt.savefig('plotResults.png')





