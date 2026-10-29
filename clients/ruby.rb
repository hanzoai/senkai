require 'net/http'
require 'json'
uri=URI((ENV['HANZO_BASE_URL']||'https://api.hanzo.ai/v1')+'/worlds')
request=Net::HTTP::Post.new(uri)
request['Authorization']='Bearer '+ENV.fetch('HANZO_API_KEY')
request['Content-Type']='application/json'
request.body=JSON.generate(model:'sekai-1-alpha',domain:'simulation')
response=Net::HTTP.start(uri.hostname,uri.port,use_ssl:uri.scheme=='https',read_timeout:30){|h|h.request(request)}
raise "API status #{response.code}" unless response.is_a?(Net::HTTPSuccess)
puts response.body
