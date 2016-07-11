import org.apache.spark.SparkContext
import org.apache.spark.SparkConf
import org.elasticsearch.spark._

sc.stop()
val sc = new SparkContext(new SparkConf()
      .setMaster("local")
      .setAppName("myApp")
      .set("es.index.auto.create", "true")
      .set("es.nodes","52.11.129.157:9200")
      )

val jsonFiles = sc.textFile("s3a://venmo-json/*/*")
jsonFiles.saveJsonToEs("venmo_test/payment")

object MyFunctions {
    def process_line(s: String) = {
        val sc = new SparkContext(new SparkConf()
      .setMaster("local")
      .setAppName("myApp")
      .set("es.index.auto.create", "true")
      .set("es.nodes","52.11.129.157:9200")
      )
      
        val lineRDD = sc.parallelize(s ::Nil)
        val df1 = sqlContext.read.json(lineRDD)
        if (df1.select(df1("transactions")(0)("target")).head()(0) != "a phone number"){
            val df1_es = df1.select(df1("transactions")(0)("target")("name"),df1("transactions")(0)("target")("id"),df1("actor")("name"),df1("actor")("id"),df1("payment_id"),df1("message"),df1("updated_time"))
            df1_es.saveToEs("spark/people2")
         }
    }
}    
val lineRDD = sc.parallelize(line :: Nil)
val df = sqlContext.read.json(lineRDD)

val lines = sc.textFile("/home/ubuntu/test1000.json")
val records = lines.take(2)
val line1RDD = sc.parallelize(records(0) ::Nil)
val df1 = sqlContext.read.json(line1RDD)


//spark-shell --jars /home/ubuntu/Downloads/spark-redis/target/spas-0.1.1-jar-with-dependencies.jar, /home/ubuntu/Downloads/jedis-jedis-2.8.1/target/jedis-2.8.1-SNAPSHOT-javadoc.jar --packages "org.elasticsearch:elasticsearch-spark_2.10:2.3.2"

jsonFiles.filter(x=>""""target": "a phone number"""".r.findFirstIn(x)==None).saveJsonToEs("filter/test")

jsonFiles.filter(x=>""""target": "a phone number"""".r.findFirstIn(x)==None).saveJsonToEs("venmo/filter")

val jsonFiles = sc.textFile("s3a://venmo-json/*/*")
jsonFiles: org.apache.spark.rdd.RDD[String] = s3a://venmo-json/*/* MapPartitionsRDD[19] at textFile at <console>:32

jsonFiles.filter(x=> !{{x contains """[{"target": "a phone number"}]"""} || {x contains """[{"target": "an email"}]"""}}).saveJsonToEs("/venmo/filter6")



