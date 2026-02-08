import scala.io.Source
import scala.math.sqrt
import scala.util.Using
import org.json4s._
import org.json4s.jackson.JsonMethods._

object HelloWorld {
  def scrapeMumbaiTemperature(): Option[Double] = {
    try {
      val url = "https://api.open-meteo.com/v1/forecast?latitude=19.0760&longitude=72.8777&current=temperature_2m&timezone=Asia/Kolkata"
      
      Using(Source.fromURL(url)) { source =>
        val jsonString = source.mkString
        val json = parse(jsonString)
        val temperature = (json \ "current" \ "temperature_2m").extract[Double]
        Some(temperature)
      }.get
    } catch {
      case e: Exception =>
        println(s"Error scraping temperature: ${e.getMessage}")
        None
    }
  }

  def main(args: Array[String]): Unit = {
    scrapeMumbaiTemperature() match {
      case Some(temp) =>
        println(s"Current temperature in Mumbai: ${temp}°C")
        val sqrtTemp = sqrt(temp)
        println(f"Square root of temperature: ${sqrtTemp}%.2f")
      case None =>
        println("Could not retrieve temperature")
    }
  }
}
