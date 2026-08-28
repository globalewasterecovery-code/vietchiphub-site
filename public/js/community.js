// 五站共享社区组件库 · community-core.js（VietChipHub 越南语本地化 vendored 副本）
// 依赖同一个 Supabase 项目里统一结构的 posts 表：
// site / kind / category / target / title / body / tags / status / cross_post_sites。
import { supabase } from '/js/supabase-client.js';

const SITE = 'vietchiphub';

export function escapeHtml(s) {
  return String(s ?? '').replace(/[&<>"']/g, (c) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
  }[c]));
}

export function formatTime(iso) {
  try {
    const d = new Date(iso);
    return d.toLocaleString('vi-VN', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' });
  } catch { return iso; }
}

// 公开可见的展示名绝不能用邮箱兜底，避免把用户邮箱暴露给其他访客。
function publicDisplayName(user) {
  const meta = (user && user.user_metadata) || {};
  if (meta.display_name) return meta.display_name;
  if (meta.full_name) return meta.full_name;
  if (meta.name) return meta.name;
  const uid = (user && user.id) || '';
  return 'Khách ' + uid.replace(/-/g, '').slice(0, 6);
}

export async function getSession() {
  const { data: { session } } = await supabase.auth.getSession();
  return session;
}

export async function renderAuthState(containerId) {
  const el = document.getElementById(containerId);
  if (!el) return null;
  const session = await getSession();
  if (session && session.user) {
    const name = (session.user.user_metadata && session.user.user_metadata.display_name) || session.user.email;
    el.innerHTML = `Đã đăng nhập: ${escapeHtml(name)} &middot; <a href="#" id="communityLogoutLink">Đăng xuất</a>`;
    const logoutLink = document.getElementById('communityLogoutLink');
    if (logoutLink) {
      logoutLink.addEventListener('click', async (e) => {
        e.preventDefault();
        await supabase.auth.signOut();
        window.location.reload();
      });
    }
  } else {
    el.innerHTML = '<a href="/dang-ky/" class="cta-join">Đăng ký</a> &middot; <a href="/dang-nhap/">Đăng nhập</a>';
  }
  return session;
}

export async function submitPost({ kind, category = null, target = null, title = null, body, tags = [] }) {
  const session = await getSession();
  if (!session || !session.user) {
    throw new Error('NEED_LOGIN');
  }
  const displayName = publicDisplayName(session.user);
  const { data, error } = await supabase
    .from('posts')
    .insert({
      user_id: session.user.id,
      display_name: displayName,
      site: SITE,
      kind,
      category,
      target,
      title,
      body,
      tags: (tags && tags.length) ? tags : [],
    })
    .select()
    .single();
  if (error) {
    if (String(error.message || '').includes('RATE_LIMITED')) throw new Error('Bạn đăng bài quá thường xuyên, vui lòng thử lại sau.');
    throw error;
  }
  return data;
}

export async function fetchPosts({ kind, category = null, target = null, tag = null, q = null, limit = 50 }) {
  let query = supabase.from('posts').select('*').eq('site', SITE).eq('kind', kind).eq('status', 'active').order('created_at', { ascending: false }).limit(limit);
  if (target !== null) query = query.eq('target', target);
  if (category !== null) query = query.eq('category', category);
  if (tag !== null) query = query.contains('tags', [tag]);
  if (q) query = query.or(`title.ilike.%${q}%,body.ilike.%${q}%`);
  const { data, error } = await query;
  if (error) throw error;
  return data || [];
}

export async function updatePost(id, body) {
  const { error } = await supabase.from('posts').update({ body, updated_at: new Date().toISOString() }).eq('id', id);
  if (error) throw error;
}

export async function deletePost(id) {
  const { error } = await supabase.from('posts').delete().eq('id', id);
  if (error) throw error;
}

export async function reportPost(id, reason = 'user_reported') {
  const session = await getSession();
  if (!session || !session.user) throw new Error('NEED_LOGIN');
  const { error } = await supabase.from('reports').insert({ post_id: id, reporter_user_id: session.user.id, reason });
  if (error) throw error;
}

const CATEGORY_LABELS = {
  'Cần mua': 'Cần mua',
  'Cung cấp': 'Cung cấp',
  'Hợp tác': 'Hợp tác',
};

export function renderPostList(containerId, posts, { emptyText = 'Chưa có nội dung. Hãy là người đầu tiên đăng.', showTitle = false, actionable = true } = {}) {
  const el = document.getElementById(containerId);
  if (!el) return;
  if (!posts.length) {
    el.innerHTML = `<p class="empty">${escapeHtml(emptyText)}</p>`;
    return;
  }
  const render = (uid) => {
    el.innerHTML = posts.map((p) => {
      const mine = actionable && uid && p.user_id === uid;
      const catPill = p.category ? `<span class="tag-pill">${escapeHtml(CATEGORY_LABELS[p.category] || p.category)}</span>` : '';
      const tagsHtml = (catPill || (p.tags && p.tags.length)) ? `<div class="post-tags">${catPill}${(p.tags||[]).map((t) => `<span class="tag-pill">${escapeHtml(t)}</span>`).join('')}</div>` : '';
      const actions = !actionable ? '' : (mine
        ? `<button type="button" class="post-action" data-act="edit" data-id="${p.id}">Sửa</button><button type="button" class="post-action" data-act="delete" data-id="${p.id}">Xóa</button>`
        : `<button type="button" class="post-action" data-act="report" data-id="${p.id}">Báo cáo</button>`);
      return `<article class="post-item" data-post-id="${p.id}">
        ${showTitle && p.title ? `<h3>${escapeHtml(p.title)}</h3>` : ''}
        ${tagsHtml}
        <p class="post-body" data-body>${escapeHtml(p.body)}</p>
        <div class="post-meta">${escapeHtml(p.display_name)} &middot; ${formatTime(p.created_at)}${p.updated_at ? ' &middot; đã sửa' : ''} <span class="post-actions">${actions}</span></div>
      </article>`;
    }).join('');
    if (!actionable) return;
    el.querySelectorAll('.post-action').forEach((btn) => {
      btn.addEventListener('click', async () => {
        const id = btn.dataset.id;
        const act = btn.dataset.act;
        const article = el.querySelector(`[data-post-id="${id}"]`);
        if (act === 'delete') {
          if (!confirm('Bạn có chắc muốn xóa nội dung này? Không thể khôi phục.')) return;
          try { await deletePost(id); article.remove(); } catch (e) { alert('Xóa thất bại: ' + (e && e.message ? e.message : e)); }
        } else if (act === 'edit') {
          const bodyEl = article.querySelector('[data-body]');
          const current = (posts.find((p) => String(p.id) === String(id)) || {}).body || '';
          const next = prompt('Sửa nội dung:', current);
          if (next === null || !next.trim()) return;
          try { await updatePost(id, next.trim()); bodyEl.textContent = next.trim(); } catch (e) { alert('Sửa thất bại: ' + (e && e.message ? e.message : e)); }
        } else if (act === 'report') {
          if (!confirm('Bạn có chắc muốn báo cáo nội dung này cho quản trị viên?')) return;
          try { await reportPost(id); btn.textContent = 'Đã báo cáo'; btn.disabled = true; } catch (e) {
            if (e && e.message === 'NEED_LOGIN') alert('Vui lòng đăng nhập trước khi báo cáo.');
            else alert('Báo cáo thất bại: ' + (e && e.message ? e.message : e));
          }
        }
      });
    });
  };
  getSession().then((session) => render(session && session.user ? session.user.id : null));
}

export function wirePostForm({ formId, msgId, kind, category = null, target = null, onSuccess }) {
  const form = document.getElementById(formId);
  if (!form) return;
  const msg = document.getElementById(msgId);
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (msg) { msg.textContent = ''; msg.className = 'msg'; }
    const bodyEl = form.querySelector('#postBody');
    const titleEl = form.querySelector('#postTitle');
    const tagsEl = form.querySelector('#postTags');
    const catEl = form.querySelector('#postCategory');
    const body = bodyEl ? bodyEl.value.trim() : '';
    const title = titleEl ? titleEl.value.trim() : null;
    const tags = tagsEl ? tagsEl.value.split(',').map((t) => t.trim()).filter(Boolean) : [];
    const cat = catEl ? catEl.value : category;
    if (!body) return;
    const btn = form.querySelector('button[type="submit"]');
    if (btn) btn.disabled = true;
    try {
      await submitPost({ kind, category: cat, target, title: title || null, body, tags });
      if (bodyEl) bodyEl.value = '';
      if (titleEl) titleEl.value = '';
      if (tagsEl) tagsEl.value = '';
      if (msg) { msg.textContent = 'Đã đăng.'; msg.className = 'msg ok'; }
      if (onSuccess) await onSuccess();
    } catch (err) {
      if (err && err.message === 'NEED_LOGIN') {
        if (msg) { msg.textContent = 'Vui lòng đăng nhập hoặc đăng ký trước khi đăng bài.'; msg.className = 'msg err'; }
      } else {
        if (msg) { msg.textContent = 'Đăng thất bại: ' + (err && err.message ? err.message : String(err)); msg.className = 'msg err'; }
      }
    } finally {
      if (btn) btn.disabled = false;
    }
  });
}
