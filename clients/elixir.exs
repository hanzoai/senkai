Application.ensure_all_started(:inets)
Application.ensure_all_started(:ssl)
base=System.get_env("HANZO_BASE_URL") || "https://api.hanzo.ai/v1"
key=System.fetch_env!("HANZO_API_KEY")
headers=[{~c"authorization",String.to_charlist("Bearer "<>key)}]
{:ok,{{_,status,_},_,body}}=:httpc.request(:post,{String.to_charlist(base<>"/worlds"),headers,~c"application/json",~c"{\"model\":\"sekai-1-alpha\",\"domain\":\"simulation\"}"},[timeout:30000,autoredirect:false],[])
if status<200 or status>=300,do:raise("API status #{status}")
IO.puts(body)
