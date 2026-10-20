ALTER TABLE vietchiphub_rfqs ADD COLUMN direction TEXT NOT NULL DEFAULT 'BUY';
ALTER TABLE vietchiphub_rfqs ADD COLUMN currency TEXT NOT NULL DEFAULT '';
ALTER TABLE vietchiphub_rfqs ADD COLUMN quantity_unit TEXT NOT NULL DEFAULT 'pcs';
ALTER TABLE vietchiphub_rfqs ADD COLUMN item_condition TEXT NOT NULL DEFAULT 'UNKNOWN';
ALTER TABLE vietchiphub_rfqs ADD COLUMN country TEXT NOT NULL DEFAULT '';
ALTER TABLE vietchiphub_rfqs ADD COLUMN tax_basis TEXT NOT NULL DEFAULT 'UNKNOWN';
ALTER TABLE vietchiphub_rfqs ADD COLUMN line_items_json TEXT NOT NULL DEFAULT '[]';
ALTER TABLE vietchiphub_rfqs ADD COLUMN request_key TEXT;
ALTER TABLE vietchiphub_rfqs ADD COLUMN payload_hash TEXT;
ALTER TABLE vietchiphub_rfqs ADD COLUMN is_test INTEGER NOT NULL DEFAULT 0;
CREATE UNIQUE INDEX IF NOT EXISTS idx_vch_request_key ON vietchiphub_rfqs(request_key) WHERE request_key IS NOT NULL;
CREATE TABLE IF NOT EXISTS vch_notification_outbox (
 rfq_id INTEGER PRIMARY KEY REFERENCES vietchiphub_rfqs(id), state TEXT NOT NULL DEFAULT 'PENDING',
 attempts INTEGER NOT NULL DEFAULT 0, next_attempt_at TEXT, provider_id TEXT, last_error TEXT,
 sent_at TEXT, delivered_at TEXT,
 created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);
CREATE INDEX IF NOT EXISTS idx_vch_outbox_pending ON vch_notification_outbox(state,next_attempt_at);
