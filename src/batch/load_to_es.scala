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


