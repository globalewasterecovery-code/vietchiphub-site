function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' },
  });
}

async function readPayload(request) {
  const type = request.headers.get('content-type') || '';
  if (type.includes('application/json')) return request.json();
  const form = await request.formData();
  const out = {};
  for (const [key, value] of form.entries()) out[key] = value;
  return out;
}

const STRING_FIELDS = [
  'company', 'contact', 'part_number', 'quantity', 'target_price',
  'delivery_requirement', 'details',
];

export async function onRequestPost({ request, env }) {
  try {
    if (!env.vietchiphub_rfq) {
      return json({ ok: false, error: 'db_binding_missing' }, 500);
    }
    const raw = await readPayload(request);
    const contact = (raw.contact || raw.email || raw.whatsapp || '').trim();
    const partNumber = (raw.part_number || raw.part || raw.sku || '').trim();
    const quantity = (raw.quantity || raw.qty || '').trim();
    const company = (raw.company || raw.name || '').trim();
    const targetPrice = (raw.target_price || '').trim();
    const deliveryReq = (raw.delivery_country || raw.delivery_requirement || '').trim();
    
    let detailsText = (raw.details || raw.additional_requirements || '').trim();
    if (raw.manufacturer) detailsText = `Manufacturer: ${raw.manufacturer.trim()}\n` + detailsText;
    if (raw.acceptable_condition) detailsText = `Acceptable Condition: ${raw.acceptable_condition.trim()}\n` + detailsText;
    if (raw.delivery_country) detailsText = `Delivery Country: ${raw.delivery_country.trim()}\n` + detailsText;
    if (raw.name) detailsText = `Contact Name: ${raw.name.trim()}\n` + detailsText;

    const language = ['vi', 'en', 'zh'].includes(String(raw.language || '').toLowerCase())
      ? String(raw.language).toLowerCase()
      : 'vi';

    if (!contact || !partNumber) {
      return json({ ok: false, error: 'missing_required_fields' }, 400);
    }
    const created_at = new Date().toISOString();
    const result = await env.vietchiphub_rfq
      .prepare(
        `INSERT INTO vietchiphub_rfqs
          (company, contact, part_number, quantity, target_price,
           delivery_requirement, details, language, status, created_at)
         VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'NEW', ?)`
      )
      .bind(
        company, contact, partNumber, quantity, targetPrice,
        deliveryReq, detailsText, language, created_at
      )
      .run();
    return json({ ok: true, id: result.meta.last_row_id }, 201);
  } catch (error) {
    return json({ ok: false, error: 'server_error', message: String(error && error.message || error) }, 500);
  }
}
