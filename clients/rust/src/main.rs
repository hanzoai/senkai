use hanzo_ml::{Device, Tensor};
use serde_json::{json, Value};
use std::{env, error::Error, time::{Instant, SystemTime, UNIX_EPOCH}};

fn base() -> String { env::var("HANZO_BASE_URL").unwrap_or("https://api.hanzo.ai/v1".into()).trim_end_matches('/').into() }
fn request(method: &str, path: &str, body: Option<Value>) -> Result<Value, Box<dyn Error>> {
    let base=base();
    if !base.starts_with("https://") && !base.starts_with("http://127.0.0.1:") && !base.starts_with("http://localhost:") {return Err("HTTPS required".into())}
    let key=env::var("HANZO_API_KEY")?;
    let agent=ureq::AgentBuilder::new().redirects(0).timeout(std::time::Duration::from_secs(30)).build();
    let req=agent.request(method,&format!("{base}{path}")).set("Authorization",&format!("Bearer {key}"));
    let response=match body{Some(b)=>req.send_json(b)?,None=>req.call()?};
    Ok(response.into_json()?)
}
fn serve() -> Result<(),Box<dyn Error>> {
    let secret=env::var("GATEWAY_API_KEY")?;
    let server=tiny_http::Server::http("127.0.0.1:8051").map_err(|e|e.to_string())?;
    for mut incoming in server.incoming_requests(){
        let supplied=incoming.headers().iter().find(|h|h.field.equiv("Authorization")).map(|h|h.value.as_str()).unwrap_or("");
        let expected=format!("Bearer {secret}");
        let auth=supplied.len()==expected.len() && supplied.bytes().zip(expected.bytes()).fold(0u8,|x,(a,b)|x|(a^b))==0;
        let url=incoming.url().to_string();let method=incoming.method().as_str().to_string();
        let allowed=(url=="/v1/worlds" || url.starts_with("/v1/worlds/")) && url.chars().all(|c|c.is_ascii_alphanumeric()||"/_-".contains(c)) && ["GET","POST"].contains(&method.as_str());
        let (code,body)=if !auth{(401,json!({"error":"unauthorized"}))}else if !allowed{(404,json!({"error":"unknown route"}))}else if incoming.body_length().unwrap_or(if method=="GET"{0}else{1_048_577})>1_048_576{(413,json!({"error":"request too large"}))}else{
            let mut raw=String::new();incoming.as_reader().read_to_string(&mut raw)?;
            let body=if raw.is_empty(){None}else{match serde_json::from_str(&raw){Ok(v)=>Some(v),Err(_)=>{incoming.respond(tiny_http::Response::from_string("invalid JSON").with_status_code(400))?;continue}}};
            match request(&method,&url[3..],body){Ok(v)=>(200,v),Err(_)=>(502,json!({"error":"upstream unavailable or refused request"}))}
        };
        incoming.respond(tiny_http::Response::from_string(body.to_string()).with_status_code(code)
            .with_header(tiny_http::Header::from_bytes("Content-Type","application/json").unwrap()))?;
    }
    Ok(())
}
fn main() -> Result<(), Box<dyn Error>> {
    let mode=env::args().nth(1).unwrap_or("client".into());
    if mode=="serve"{return serve()}
    let start=Instant::now();
    let world=request("POST","/worlds",Some(json!({"model":"sekai-1-alpha","domain":"simulation"})))?;
    let ms=start.elapsed().as_secs_f64()*1000.;
    if mode=="ml" {
        // Public application-owned unit conversion. No model encoder or weights.
        let features=(&Tensor::new(&[10f32,20.,0.,0.],&Device::Cpu)?/100f64)?.to_vec1::<f32>()?;
        let world_id=world["id"].as_str().ok_or("world id missing")?;
        let stamp=SystemTime::now().duration_since(UNIX_EPOCH)?.as_secs_f64();
        println!("{}",request("POST",&format!("/worlds/{world_id}/events"),Some(json!({"event_id":format!("rust-{stamp}"),"entity_id":"sensor_a","timestamp":stamp,"modality":"telemetry","features":features})))?);
    } else if mode=="research" {
        let token=env::var("RESEARCH_API_KEY").map_err(|e|e.to_string()).or_else(|_|hanzo_research::token().map_err(|e|e.to_string()))?;
        let api=hanzo_research::Api::new(&env::var("RESEARCH_BASE").unwrap_or("https://api.hanzo.ai".into()),"",token)?;
        let id=format!("sekai-alpha-api-{}",SystemTime::now().duration_since(UNIX_EPOCH)?.as_nanos());
        let _:Value=api.post("benchmarks",&json!({"benchmarks":[{"id":"sekai.alpha.api-create","title":"Alpha API creation latency","metric":"latency_ms"}]}))?;
        let _:Value=api.post("runs",&json!({"runs":[{"id":id,"benchmark":"sekai.alpha.api-create","system":"sekai-1-alpha","questions":1,"answered":1,"ended":hanzo_research::now(),"visibility":"private","trainable":false,"publishable":false,"measures":[{"category":"all","metric":"latency_ms","value":ms}]}]}))?;
        println!("Recorded privately: {id}");
    } else {println!("{world}")}
    Ok(())
}
