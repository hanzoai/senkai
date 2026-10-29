using System; using System.Net.Http; using System.Text;
var key=Environment.GetEnvironmentVariable("HANZO_API_KEY")??throw new Exception("Set HANZO_API_KEY");
var url=(Environment.GetEnvironmentVariable("HANZO_BASE_URL")??"https://api.hanzo.ai/v1")+"/worlds";
using var client=new HttpClient(new HttpClientHandler{AllowAutoRedirect=false}){Timeout=TimeSpan.FromSeconds(30)};
using var req=new HttpRequestMessage(HttpMethod.Post,url);
req.Headers.Authorization=new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer",key);
req.Content=new StringContent("{\"model\":\"sekai-1-alpha\",\"domain\":\"simulation\"}",Encoding.UTF8,"application/json");
using var response=await client.SendAsync(req);response.EnsureSuccessStatusCode();Console.WriteLine(await response.Content.ReadAsStringAsync());
