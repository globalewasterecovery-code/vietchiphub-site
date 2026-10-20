(function () {
  const form = document.getElementById('rfq-form');
  if (!form) return;

  const msg = document.getElementById('rfq-msg');
  const lang = form.dataset.lang || document.documentElement.lang || 'vi';
  const messages = {
    vi: {
      ok: 'Đã nhận RFQ. Cảm ơn bạn, đội ngũ sẽ kiểm tra và phản hồi thủ công.',
      err: 'Không gửi được RFQ. Vui lòng kiểm tra thông tin và thử lại.',
    },
    en: {
      ok: 'RFQ received. Thank you — our team will review it manually and follow up.',
      err: 'Could not submit the RFQ. Please check your details and try again.',
    },
    zh: {
      ok: '询价已收到。感谢提交，我们会人工审核并跟进。',
      err: '提交失败，请检查信息后重试。',
    },
  };
  const text = messages[lang] || messages.en;

  const params = new URLSearchParams(window.location.search);
  const partVal = params.get('part') || params.get('part_number') || params.get('sku') || params.get('bom');
  const catVal = params.get('category');
  if (partVal && form.elements.part_number && !form.elements.part_number.value) {
    form.elements.part_number.value = partVal;
  }
  if (catVal && form.elements.details && !form.elements.details.value) {
    form.elements.details.value = 'Category: ' + catVal;
  }

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const button = form.querySelector('button[type="submit"]');
    const data = new FormData(form);
    data.set('language', lang);
    const payload = Object.fromEntries(data.entries());
    if (!payload.contact || !payload.part_number) {
      if (msg) {
        msg.textContent = text.err;
        msg.style.color = '#b3261e';
      }
      return;
    }
    if (msg) {
      msg.textContent = '';
    }
    if (button) button.disabled = true;
    try {
      const response = await fetch('/api/rfq', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const result = await response.json();
      if (!response.ok || !result.ok) throw new Error(result.error || 'submit_failed');
      form.reset();
      if (msg) {
        msg.textContent = text.ok;
        msg.style.color = '#0a7d3c';
        msg.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }
    } catch (error) {
      if (msg) {
        msg.textContent = text.err;
        msg.style.color = '#b3261e';
      }
    } finally {
      if (button) button.disabled = false;
    }
  });
})();
