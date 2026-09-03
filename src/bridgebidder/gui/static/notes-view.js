/**
 * notes-view.js — the list of notes waiting to be turned into rule changes.
 *
 * This is a reading surface, not a workflow. The notes are written from the
 * Deal Explorer and acted on in a Claude session that edits the YAML; all this
 * screen does is show what has been captured, let a note be marked done once
 * its fix has landed, and hand over the file path to point the session at.
 */

import { toast } from './ui.js';

async function apiFetch(path, opts = {}) {
  const res = await fetch(path, {
    headers: { 'Content-Type': 'application/json', ...opts.headers },
    ...opts,
  });
  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(`${res.status} ${res.statusText}${text ? ': ' + text : ''}`);
  }
  return res.json();
}

function esc(s) {
  return String(s ?? '').replace(/[<>&"]/g, c =>
    ({ '<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;' }[c]));
}

function fmtWhen(iso) {
  try {
    return new Date(iso).toLocaleString('he-IL', {
      day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit',
    });
  } catch { return iso; }
}

const SEATS = ['W', 'N', 'E', 'S'];

/** One auction as `W:1D N:1S[open_1S] …`, so a note reads without the app. */
function auctionLine(deal, key) {
  const t = (deal || {})[key] || {};
  const calls = t.auction || [];
  if (!calls.length) return '';
  const rules = {};
  for (const c of (t.our_calls || [])) rules[c.n] = c.rule;
  const start = Math.max(0, SEATS.indexOf(deal.dealer));
  return calls.map((call, n) => {
    const seat = SEATS[(start + n) % 4];
    const rule = rules[n];
    return `${seat}:${call}${rule ? `[${rule}]` : ''}`;
  }).join(' ');
}

export class NotesView {
  constructor(root) {
    this.root = root;
    this.notes = [];
    this.showDone = false;
  }

  render() {
    this.root.innerHTML = /* html */`
      <div class="notes-view">
        <div class="notes-header">
          <div>
            <div class="sidebar-heading">Notes</div>
            <div class="sidebar-sub" id="nv-count">Loading…</div>
          </div>
          <label class="notes-toggle">
            <input type="checkbox" id="nv-show-done"> show done
          </label>
        </div>
        <div class="notes-howto">
          Saved to <code>data/notes/notes.jsonl</code>, with a readable copy at
          <code>data/notes/NOTES.md</code>. Point a Claude session at either and
          ask it to work through the open ones; mark a note done once its change
          is in the rulebook.
        </div>
        <div id="nv-list" class="notes-list"></div>
      </div>`;

    document.getElementById('nv-show-done').addEventListener('change', e => {
      this.showDone = e.target.checked;
      this._renderList();
    });
    this._load();
  }

  destroy() {}

  async _load() {
    try {
      const data = await apiFetch('/api/notes');
      this.notes = data.notes || [];
      this._renderList();
    } catch (err) {
      document.getElementById('nv-list').innerHTML =
        `<div class="error-banner">${esc(err.message)}</div>`;
    }
  }

  _renderList() {
    const list = document.getElementById('nv-list');
    const open = this.notes.filter(n => n.status !== 'done');
    const done = this.notes.filter(n => n.status === 'done');
    document.getElementById('nv-count').textContent =
      `${open.length} open · ${done.length} done`;

    const shown = this.showDone ? [...open, ...done] : open;
    if (!shown.length) {
      list.innerHTML = `<div class="notes-empty">${
        this.notes.length
          ? 'Nothing open. Tick “show done” to see the rest.'
          : 'No notes yet. Find a board, click one of our bids, and describe what looks wrong.'
      }</div>`;
      return;
    }

    list.innerHTML = shown.map(n => this._card(n)).join('');
    list.querySelectorAll('[data-toggle]').forEach(btn => {
      btn.addEventListener('click', () => this._setStatus(
        btn.dataset.toggle, btn.dataset.status === 'done' ? 'open' : 'done'));
    });
    list.querySelectorAll('[data-delete]').forEach(btn => {
      btn.addEventListener('click', () => this._delete(btn.dataset.delete));
    });
  }

  _card(n) {
    const deal = n.deal;
    const bid = n.bid;
    const isDone = n.status === 'done';
    const hands = deal && deal.hands
      ? Object.entries(deal.hands).map(([seat, h]) =>
          `<span class="nv-hand"><b>${seat}</b> ${esc(h)}</span>`).join('')
      : '';
    return /* html */`
      <div class="note-card ${isDone ? 'is-done' : ''}">
        <div class="note-card-head">
          <span class="note-id">${esc(n.id)}</span>
          ${deal ? `<span class="note-ref">${esc(deal.ref)}</span>` : ''}
          <span class="note-when">${fmtWhen(n.created_at)}</span>
        </div>

        <div class="note-text">${esc(n.text).replace(/\n/g, '<br>')}</div>

        ${bid ? /* html */`
          <div class="note-bid">
            About <b>${esc(bid.seat)}'s ${esc(bid.call)}</b>
            (call ${bid.n}, table ${esc(bid.table)}) from
            <code>${esc(bid.rule_id)}</code> in <code>${esc(bid.context_id)}</code>
          </div>` : ''}

        ${deal ? /* html */`
          <details class="note-detail">
            <summary>Board — dealer ${esc(deal.dealer)}, vul ${esc(deal.vul)},
              BEN won by ${Math.abs(deal.imp_margin || 0)} IMP</summary>
            <div class="nv-hands">${hands}</div>
            <div class="nv-auction"><b>A</b> (${esc(deal.table_a?.our_side)} us,
              ${esc(deal.table_a?.contract)}) <code>${esc(auctionLine(deal, 'table_a'))}</code></div>
            <div class="nv-auction"><b>B</b> (${esc(deal.table_b?.our_side)} us,
              ${esc(deal.table_b?.contract)}) <code>${esc(auctionLine(deal, 'table_b'))}</code></div>
          </details>` : ''}

        <div class="note-actions">
          <button class="btn btn-secondary btn-sm"
                  data-toggle="${esc(n.id)}" data-status="${esc(n.status)}">
            ${isDone ? 'Reopen' : 'Mark done'}
          </button>
          <button class="btn btn-ghost btn-sm" data-delete="${esc(n.id)}">Delete</button>
        </div>
      </div>`;
  }

  async _setStatus(id, status) {
    try {
      await apiFetch(`/api/notes/${id}/status`, {
        method: 'POST', body: JSON.stringify({ status }),
      });
      await this._load();
    } catch (err) {
      toast(`Could not update ${id}: ${err.message}`, 'error');
    }
  }

  async _delete(id) {
    // Deliberately not confirmed: a note is cheap to rewrite, and the record
    // is a tracked file, so a mistaken delete is recoverable from git.
    try {
      await apiFetch(`/api/notes/${id}`, { method: 'DELETE' });
      toast(`${id} deleted.`, 'success');
      await this._load();
    } catch (err) {
      toast(`Could not delete ${id}: ${err.message}`, 'error');
    }
  }
}
