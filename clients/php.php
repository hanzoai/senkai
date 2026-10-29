<?php
$key=getenv('HANZO_API_KEY');if(!$key)throw new Exception('Set HANZO_API_KEY');
$base=getenv('HANZO_BASE_URL')?:'https://api.hanzo.ai/v1';
$context=stream_context_create(['http'=>['method'=>'POST','timeout'=>30,'follow_location'=>0,'header'=>"Authorization: Bearer $key\r\nContent-Type: application/json\r\n",'content'=>json_encode(['model'=>'sekai-1-alpha','domain'=>'simulation'])]]);
$result=file_get_contents($base.'/worlds',false,$context);if($result===false)throw new Exception('API request failed');echo $result.PHP_EOL;
