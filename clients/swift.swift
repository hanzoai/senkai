import Foundation
#if canImport(FoundationNetworking)
import FoundationNetworking
#endif
let env=ProcessInfo.processInfo.environment
guard let key=env["HANZO_API_KEY"] else{fatalError("Set HANZO_API_KEY")}
let base=env["HANZO_BASE_URL"] ?? "https://api.hanzo.ai/v1"
var req=URLRequest(url:URL(string:base+"/worlds")!);req.httpMethod="POST";req.timeoutInterval=30
req.setValue("Bearer "+key,forHTTPHeaderField:"Authorization");req.setValue("application/json",forHTTPHeaderField:"Content-Type")
req.httpBody=try JSONSerialization.data(withJSONObject:["model":"sekai-1-alpha","domain":"simulation"])
let (data,response)=try await URLSession.shared.data(for:req)
guard let http=response as? HTTPURLResponse,(200..<300).contains(http.statusCode) else{fatalError("API refused request")}
print(String(data:data,encoding:.utf8)!)
