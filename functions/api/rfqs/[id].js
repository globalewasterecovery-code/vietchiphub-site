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

const ALLOWED = new Set(['NEW', 'REVIEWING', 'QUOTED', 'CLOSED']);

export async function onRequestPatch({ request, env, params }) {
  if (!authorized(request, env)) return json({ ok: false, error: 'unauthorized' }, 401);
  const id = Number(params.id);
  if (!Number.isInteger(id) || id <= 0) return json({ ok: false, error: 'bad_id' }, 400);
  let body;
  try {
    body = await request.json();
  } catch {
    return json({ ok: false, error: 'bad_json' }, 400);
  }
  const status = String(body.status || '').toUpperCase();
  if (!ALLOWED.has(status)) return json({ ok: false, error: 'bad_status' }, 400);
  try {
    const result = await env.vietchiphub_rfq
      .prepare(
        `UPDATE vietchiphub_rfqs
         SET status = ?, updated_at = strftime('%Y-%m-%dT%H:%M:%fZ', 'now')
         WHERE id = ?`
      )
      .bind(status, id)
      .run();
    if (!result.meta.changes) return json({ ok: false, error: 'not_found' }, 404);
    return json({ ok: true, id, status });
  } catch (error) {
    return json({ ok: false, error: 'server_error', message: String(error && error.message || error) }, 500);
  }
}
