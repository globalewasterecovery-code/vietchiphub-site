CREATE TABLE IF NOT EXISTS vietchiphub_rfqs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  company TEXT NOT NULL DEFAULT '',
  contact TEXT NOT NULL,
  part_number TEXT NOT NULL,
  quantity TEXT NOT NULL DEFAULT '',
  target_price TEXT NOT NULL DEFAULT '',
  delivery_requirement TEXT NOT NULL DEFAULT '',
  details TEXT NOT NULL DEFAULT '',
  language TEXT NOT NULL DEFAULT 'vi',
  status TEXT NOT NULL DEFAULT 'NEW',
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
  updated_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_vietchiphub_rfqs_status_created
  ON vietchiphub_rfqs(status, created_at);
