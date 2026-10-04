(function () {
  const KEY_STORE = 'vch_staff_key';
  const listEl = document.getElementById('rfqRows');
  const msgEl = document.getElementById('staffMsg');
  const countEl = document.getElementById('newCount');
  const loginPanel = document.getElementById('loginPanel');
  const board = document.getElementById('board');
  const tokenInput = document.getElementById('staffKeyInput');

  function say(text, ok) {
    if (!msgEl) return;
    msgEl.textContent = text;
    msgEl.style.color = ok ? '#0a7d3c' : '#b3261e';
  }

  function esc(value) {
    const el = document.createElement('div');
    el.textContent = value == null ? '' : String(value);
    return el.innerHTML;
  }

  async function api(path, options = {}) {
    const key = sessionStorage.getItem(KEY_STORE);
    const headers = Object.assign({}, options.headers || {}, {
      authorization: 'Bearer ' + key,
      'content-type': 'application/json',
    });
    const response = await fetch(path, Object.assign({}, options, { headers }));
    return response.json();
  }

  async function updateStatus(id, status) {
    const result = await api('/api/rfqs/' + id, {
      method: 'PATCH',
      body: JSON.stringify({ status }),
    });
    if (!result.ok) {
      say('Update failed: ' + (result.error || 'unknown'), false);
      return;
    }
    await load();
  }

  function render(rows) {
    const newRows = (rows || []).filter((r) => r.status === 'NEW');
    if (countEl) countEl.textContent = String(newRows.length);
    listEl.innerHTML = '';
    if (!rows || !rows.length) {
      listEl.innerHTML = '<tr><td colspan="12">No RFQs yet.</td></tr>';
      return;
    }
    for (const r of rows) {
      const tr = document.createElement('tr');
      const cells = [
        r.id, r.created_at, r.language, r.company, r.contact, r.part_number,
        r.quantity, r.target_price, r.delivery_requirement, r.details, r.status,
      ];
      for (const value of cells) {
        const td = document.createElement('td');
        td.textContent = value == null ? '' : value;
        tr.appendChild(td);
      }
      const actions = document.createElement('td');
      for (const status of ['NEW', 'REVIEWING', 'QUOTED', 'CLOSED']) {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.textContent = status;
        btn.style.cssText = 'margin:2px;font-size:11px;padding:4px 6px;border-radius:6px;border:1px solid #b9c8d8;background:' + (r.status === status ? '#0757d9' : '#fff') + ';color:' + (r.status === status ? '#fff' : '#081a2d') + ';cursor:pointer';
        btn.addEventListener('click', () => updateStatus(r.id, status));
        actions.appendChild(btn);
      }
      tr.appendChild(actions);
      listEl.appendChild(tr);
    }
  }

  async function load() {
    if (!sessionStorage.getItem(KEY_STORE)) return;
    try {
      const result = await api('/api/rfqs');
      if (!result.ok) {
        sessionStorage.removeItem(KEY_STORE);
        showLogin();
        say('Unauthorized. Enter the staff key.', false);
        return;
      }
      board.style.display = 'block';
      loginPanel.style.display = 'none';
      render(result.rows || []);
    } catch (error) {
      say('Load failed: ' + error.message, false);
    }
  }

  function showLogin() {
    board.style.display = 'none';
    loginPanel.style.display = 'block';
  }

  const unlock = document.getElementById('unlockBtn');
  if (unlock) {
    unlock.addEventListener('click', () => {
      const key = (tokenInput.value || '').trim();
      if (!key) return;
      sessionStorage.setItem(KEY_STORE, key);
      load();
    });
  }

  const logout = document.getElementById('logoutBtn');
  if (logout) {
    logout.addEventListener('click', () => {
      sessionStorage.removeItem(KEY_STORE);
      showLogin();
    });
  }

  showLogin();
  if (sessionStorage.getItem(KEY_STORE)) load();
})();
