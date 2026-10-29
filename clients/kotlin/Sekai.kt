import java.net.URI
import java.net.http.*
import java.time.Duration
fun main(){val key=System.getenv("HANZO_API_KEY")?:error("Set HANZO_API_KEY");val base=System.getenv("HANZO_BASE_URL")?:"https://api.hanzo.ai/v1";val req=HttpRequest.newBuilder(URI.create("$base/worlds")).timeout(Duration.ofSeconds(30)).header("Authorization","Bearer $key").header("Content-Type","application/json").POST(HttpRequest.BodyPublishers.ofString("""{"model":"sekai-1-alpha","domain":"simulation"}""")).build();val r=HttpClient.newHttpClient().send(req,HttpResponse.BodyHandlers.ofString());check(r.statusCode()/100==2);println(r.body())}
