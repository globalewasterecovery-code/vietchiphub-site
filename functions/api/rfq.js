const reply = (data, status = 200) => new Response(JSON.stringify(data), {
  status, headers: {'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store'},
});
const clean = (value, max = 500) => typeof value === 'string' ? value.trim().slice(0, max) : '';
const choice = (v, allowed, fallback) => allowed.includes(v) ? v : fallback;
export async function onRequestPost({request, env}) {
  if (!env.vietchiphub_rfq) return reply({ok:false,error:'db_binding_missing'},503);
  const origin = request.headers.get('origin');
  if (origin && origin !== new URL(request.url).origin) return reply({ok:false,error:'origin_mismatch'},403);
  if (Number(request.headers.get('content-length') || 0) > 50000) return reply({ok:false,error:'payload_too_large'},413);
  let raw;
  try {
    const text = await request.text();
    if (text.length > 50000) return reply({ok:false,error:'payload_too_large'},413);
    raw = (request.headers.get('content-type') || '').includes('application/json') ? JSON.parse(text) : Object.fromEntries(new URLSearchParams(text));
    if (!raw || typeof raw !== 'object' || Array.isArray(raw)) throw Error('bad_payload');
  } catch {return reply({ok:false,error:'bad_payload'},400);}
  if (clean(raw.website)) return reply({ok:false,error:'invalid_submission'},400);
  const contact = clean(raw.contact || raw.email || raw.whatsapp,300);
  const part = clean(raw.part_number || raw.part || raw.sku,300);
  const direction = choice(raw.direction,['BUY','SELL'],'BUY');
  if (raw.direction && raw.direction !== direction) return reply({ok:false,error:'invalid_direction'},400);
  const currency = clean(raw.currency,3).toUpperCase();
  if (currency && !['USD','CNY','VND','EUR','HKD','JPY'].includes(currency)) return reply({ok:false,error:'invalid_currency'},400);
  let items = raw.items || [];
  if (!Array.isArray(items) || items.length > 100) return reply({ok:false,error:'invalid_items'},400);
  items = items.map(x => ({part_number:clean(x?.part_number,300),quantity:clean(String(x?.quantity ?? ''),100),target_price:clean(String(x?.target_price ?? ''),100)}));
  if (items.some(x=>!x.part_number || !/^\d+(\.\d+)?$/.test(x.quantity) || Number(x.quantity)<=0 || (x.target_price && (!/^\d+(\.\d+)?$/.test(x.target_price) || Number(x.target_price)<=0))))
    return reply({ok:false,error:'invalid_item_values'},400);
  if (!contact || (!part && !items.length)) return reply({ok:false,error:'missing_required_fields'},400);
  const requestKey=clean(raw.request_key,100) || crypto.randomUUID();
  if (!/^[a-zA-Z0-9_-]{8,100}$/.test(requestKey)) return reply({ok:false,error:'bad_request_key'},400);
  const language=choice(raw.language,['vi','en','zh'],'vi');
  const details=[raw.manufacturer && `Requested manufacturer: ${clean(raw.manufacturer)}`,raw.name && `Contact name: ${clean(raw.name)}`,clean(raw.details || raw.additional_requirements,10000)].filter(Boolean).join('\n');
  const condition=choice(raw.item_condition,['NEW','USED_TESTED','REFURBISHED','UNKNOWN'],'UNKNOWN');
  const tax=choice(raw.tax_basis,['INCLUDED','EXCLUDED','UNKNOWN'],'UNKNOWN');
  const isTest=raw.is_test===true || /IS_TEST=TRUE/i.test(details) ? 1 : 0;
  const content=JSON.stringify({company:clean(raw.company || raw.name),contact,part,quantity:raw.quantity || raw.qty || '',price:raw.target_price || '',details,direction,currency,language,items,condition,tax,country:clean(raw.country || raw.delivery_country),delivery:clean(raw.delivery_requirement || raw.delivery_country),unit:raw.quantity_unit || 'pcs',isTest});
  const payloadHash=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(content))),b=>b.toString(16).padStart(2,'0')).join('');
  try {
    const db=env.vietchiphub_rfq;
    const prior=await db.prepare('SELECT payload_hash FROM vietchiphub_rfqs WHERE request_key=?').bind(requestKey).first();
    if(prior && prior.payload_hash!==payloadHash)return reply({ok:false,error:'request_key_conflict'},409);
    await db.batch([
      db.prepare(`INSERT OR IGNORE INTO vietchiphub_rfqs
        (company,contact,part_number,quantity,target_price,delivery_requirement,details,language,status,created_at,
         direction,currency,quantity_unit,item_condition,country,tax_basis,line_items_json,request_key,is_test,payload_hash)
        VALUES (?,?,?,?,?,?,?,?,'NEW',?,?,?,?,?,?,?,?,?,?,?)`)
        .bind(clean(raw.company || raw.name),contact,part || 'BATCH BOM',clean(String(raw.quantity || raw.qty || '')),clean(String(raw.target_price || '')),
          clean(raw.delivery_requirement || raw.delivery_country),details,language,new Date().toISOString(),direction,currency,
          choice(raw.quantity_unit,['pcs','lots','hours'],'pcs'),condition,clean(raw.country || raw.delivery_country,100),tax,JSON.stringify(items),requestKey,isTest,payloadHash),
      db.prepare(`INSERT OR IGNORE INTO vch_notification_outbox(rfq_id) SELECT id FROM vietchiphub_rfqs WHERE request_key=?`).bind(requestKey),
    ]);
    const row=await db.prepare('SELECT id, direction, created_at, payload_hash FROM vietchiphub_rfqs WHERE request_key=?').bind(requestKey).first();
    if(row.payload_hash!==payloadHash)return reply({ok:false,error:'request_key_conflict'},409);
    return reply({ok:true,id:row.id,direction:row.direction,notification:'QUEUED'},201);
  } catch {return reply({ok:false,error:'submission_failed'},503);}
}
