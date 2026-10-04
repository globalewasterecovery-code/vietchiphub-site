function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' },
  });
}

function authorized(request, env) {
  const expected = env.STAFF_KEY;
  if (!expected) return false;
  const header = request.headers.get('authorization') || '';
  return header === `Bearer ${expected}`;
}

export async function onRequestGet({ request, env }) {
  if (!authorized(request, env)) return json({ ok: false, error: 'unauthorized' }, 401);
  try {
    const { results } = await env.vietchiphub_rfq
      .prepare(
        `SELECT id, company, contact, part_number, quantity, target_price,
                delivery_requirement, details, language, status, created_at, updated_at
         FROM vietchiphub_rfqs
         ORDER BY
           CASE status WHEN 'NEW' THEN 0 WHEN 'REVIEWING' THEN 1 WHEN 'QUOTED' THEN 2 ELSE 3 END,
           created_at DESC`
      )
      .all();
    return json({ ok: true, rows: results || [] });
  } catch (error) {
    return json({ ok: false, error: 'server_error', message: String(error && error.message || error) }, 500);
  }
}
