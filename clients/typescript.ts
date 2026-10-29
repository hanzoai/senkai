const base: string=(process.env.HANZO_BASE_URL||'https://api.hanzo.ai/v1').replace(/\/$/,'');
const key=process.env.HANZO_API_KEY;
if(!key) throw new Error('Set HANZO_API_KEY');
const response=await fetch(base+'/worlds',{method:'POST',redirect:'error',headers:{Authorization:'Bearer '+key,'Content-Type':'application/json'},body:JSON.stringify({model:'sekai-1-alpha',domain:'simulation'})});
if(!response.ok) throw new Error('API status '+response.status);
console.log(await response.json());
export {};
