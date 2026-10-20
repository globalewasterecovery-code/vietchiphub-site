const allowed=['page_view','cta_click','form_start','form_success','form_error','catalog_filter'];
export async function onRequestPost({request,env}){
 const origin=request.headers.get('origin');if(origin&&origin!==new URL(request.url).origin)return new Response(null,{status:403});
 try{const t=await request.text();if(t.length>1000)return new Response(null,{status:413});const p=JSON.parse(t);if(!allowed.includes(p.event)||typeof p.path!=='string'||!/^\/[A-Za-z0-9_\-/]*$/.test(p.path)||p.path.length>180)return new Response(null,{status:400});
 const db=env.leads||env.vietchiphub_rfq;await db.prepare("INSERT INTO conversion_daily(day,event,path,count) VALUES(date('now'),?,?,1) ON CONFLICT(day,event,path) DO UPDATE SET count=count+1").bind(p.event,p.path).run();return new Response(null,{status:204,headers:{'cache-control':'no-store'}});
 }catch{return new Response(null,{status:503})}
}
