function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' },
  });
}

export async function onRequestGet({ env }) {
  try {
    const db = env.vietchiphub_rfq;
    if (!db) return json({ ok: false, error: 'db_binding_missing' }, 500);
    await db.prepare('SELECT 1 AS ok').first();
    return json({ ok: true, db: 'vietchiphub_rfq' });
  } catch (error) {
    return json({ ok: false, error: 'server_error', message: String(error && error.message || error) }, 500);
  }
}
