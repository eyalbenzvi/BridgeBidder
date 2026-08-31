/**
 * proposals-view.js — Proposals Review
 *
 * Lists submitted rule-change proposals. For each proposal the user can
 * run a corpus test (12,000-board replay), inspect live progress, view
 * the final verdict, and accept or reject the proposal.
 */

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/** Small fetch wrapper that throws on non-2xx */
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

/** Build a WebSocket URL relative to the current page */
function wsUrl(path) {
  const proto = location.protocol === 'https:' ? 'wss:' : 'ws:';
  return `${proto}//${location.host}${path}`;
}

/** Format date in Israeli locale */
function fmtDate(iso) {
  try {
    return new Date(iso).toLocaleDateString('he-IL', {
      year: 'numeric', month: '2-digit', day: '2-digit',
    });
  } catch {
    return iso;
  }
}

/** Format IMP delta: sign + value, CSS class */
function fmtImp(n) {
  const abs  = Math.abs(n);
  const sign = n > 0 ? '+' : n < 0 ? '−' : '';
  return { str: `${sign}${abs}`, cls: n > 0 ? 'pos' : n < 0 ? 'neg' : 'zero' };
}

/** Convert a patch object to a human-readable string */
function humanizePatch(patch) {
  switch (patch.type) {
    case 'modify_rule': {
      const parts = Object.entries(patch.changes || {}).map(([field, ch]) => {
        const before = JSON.stringify(ch.before);
        const after  = JSON.stringify(ch.after);
        return `${field}: ${before} → ${after}`;
      });
      return `Modified ${patch.rule_id}: ${parts.join(', ')}`;
    }
    case 'add_exception':
      return `Added exception to ${patch.rule_id}`;
    case 'add_rule':
      return `Added new rule to ${patch.context_id}`;
    default:
      return JSON.stringify(patch);
  }
}

/** Status string → badge CSS class */
function statusClass(status) {
  return ({
    pending:    'pending',
    testing:    'testing',
    accepted:   'accepted',
    rejected:   'rejected',
  })[status?.toLowerCase()] || 'pending';
}

// ---------------------------------------------------------------------------
// Class
// ---------------------------------------------------------------------------

export class ProposalsView {
  constructor(root) {
    this.root = root;
    /** @type {Array<object>} */
    this.proposals = [];
    /** @type {object|null} */
    this.selectedProposal = null;
    /** @type {WebSocket|null} */
    this.testWs = null;
    /** @type {object} */
    this.testProgress = { board: 0, total: 12000, changed: 0, delta_imps: 0 };
    /** @type {boolean} */
    this._testing = false;
  }

  // -------------------------------------------------------------------------
  // Lifecycle
  // -------------------------------------------------------------------------

  render() {
    this.root.innerHTML = /* html */`
      <div class="proposals-view">

        <!-- Left sidebar: proposal list -->
        <div class="proposals-sidebar">
          <div class="sidebar-header">
            <div class="sidebar-heading">Proposals</div>
            <div class="sidebar-sub">Rule-change submissions</div>
          </div>
          <div class="proposals-list" id="pv-list">
            <div class="proposals-empty-sidebar">Loading…</div>
          </div>
        </div>

        <!-- Right panel: proposal detail -->
        <div class="proposals-detail" id="pv-detail">
          <div class="proposals-empty-detail">
            <div style="font-size:2rem;opacity:0.2">♠♥♦♣</div>
            <div>Select a proposal to review it.</div>
          </div>
        </div>

      </div>`;

    this._loadProposals();
  }

  destroy() {
    this._closeTestWs();
  }

  // -------------------------------------------------------------------------
  // Load proposals list
  // -------------------------------------------------------------------------

  async _loadProposals() {
    try {
      const data = await apiFetch('/api/proposals');
      this.proposals = Array.isArray(data) ? data : (data.proposals || []);
      this._renderProposalList(this.proposals);
    } catch (err) {
      document.getElementById('pv-list').innerHTML =
        `<div class="error-banner" style="margin:8px">${err.message}</div>`;
    }
  }

  _renderProposalList(proposals) {
    const list = document.getElementById('pv-list');
    if (!list) return;

    if (proposals.length === 0) {
      list.innerHTML = `<div class="proposals-empty-sidebar">No proposals yet.</div>`;
      return;
    }

    list.innerHTML = proposals.map(p => {
      const sc     = statusClass(p.status);
      const date   = fmtDate(p.created_at || p.date || '');
      const npatch = (p.patches || []).length;
      const pSummary = npatch === 1 ? '1 patch' : `${npatch} patches`;
      return /* html */`
        <div class="proposal-card" data-id="${p.id}" id="pcard-${p.id}">
          <div class="proposal-card-name">${this._esc(p.name)}</div>
          <div class="proposal-card-meta">
            <span>${date}</span>
            <span class="status-badge ${sc}">${p.status || 'pending'}</span>
          </div>
          <div class="proposal-card-patches">${pSummary}</div>
        </div>`;
    }).join('');

    list.querySelectorAll('.proposal-card').forEach(card => {
      card.addEventListener('click', () => this._selectProposal(card.dataset.id));
    });
  }

  // -------------------------------------------------------------------------
  // Load & render proposal detail
  // -------------------------------------------------------------------------

  async _selectProposal(id) {
    // Highlight
    document.querySelectorAll('.proposal-card.selected').forEach(c => c.classList.remove('selected'));
    document.getElementById(`pcard-${id}`)?.classList.add('selected');

    const detail = document.getElementById('pv-detail');
    detail.innerHTML = `<div style="padding:24px;color:var(--text-sub)">Loading…</div>`;

    try {
      const proposal = await apiFetch(`/api/proposals/${id}`);
      this.selectedProposal = proposal;
      this._renderProposalDetail(proposal);
    } catch (err) {
      detail.innerHTML = `<div class="error-banner" style="margin:24px">${err.message}</div>`;
    }
  }

  _renderProposalDetail(p) {
    const detail  = document.getElementById('pv-detail');
    const sc      = statusClass(p.status);
    const date    = fmtDate(p.created_at || p.date || '');
    const patches = (p.patches || []).map(pt =>
      `<div class="patch-display-item">${this._esc(humanizePatch(pt))}</div>`
    ).join('');

    // Deal reference
    const dealRef = p.deal_ref ? this._dealRefHtml(p.deal_ref) : '';

    // Corpus test result (if available)
    const resultHtml = p.test_result
      ? this._buildResultHtml(p.test_result)
      : '';

    // Can we test?
    const canTest = ['pending', 'accepted', 'rejected'].includes(p.status?.toLowerCase())
      || !p.status;
    const testBtnLabel = p.test_result ? 'Re-test' : 'Run Corpus Test';

    // Accept / reject (for pending)
    const acceptRejectHtml = (p.status === 'pending' || !p.status)
      ? /* html */`
          <div class="result-actions mt-16">
            <button class="btn btn-primary"  id="pv-btn-accept">Accept</button>
            <button class="btn btn-danger"   id="pv-btn-reject">Reject</button>
          </div>`
      : '';

    detail.innerHTML = /* html */`
      <div class="proposal-detail-header">
        <div>
          <div class="proposal-detail-name">${this._esc(p.name)}</div>
        </div>
        <span class="status-badge ${sc}">${p.status || 'pending'}</span>
      </div>
      <div class="proposal-detail-date">${date}</div>

      ${p.note ? `<div class="proposal-note">${this._esc(p.note)}</div>` : ''}

      ${dealRef ? /* html */`
      <div class="proposal-section">
        <div class="proposal-section-label">Triggering Deal</div>
        ${dealRef}
      </div>` : ''}

      <div class="proposal-section">
        <div class="proposal-section-label">Patches (${(p.patches || []).length})</div>
        <div class="patches-list">${patches || '<div style="color:var(--text-sub);font-size:0.83rem">No patches.</div>'}</div>
      </div>

      <div class="proposal-section">
        <div class="proposal-section-label">Corpus Test</div>
        <div id="pv-test-area">
          ${p.test_result
            ? resultHtml
            : `<div style="color:var(--text-sub);font-size:0.83rem;margin-bottom:12px">
                 Not yet tested against the 12,000-board corpus.
               </div>`
          }
          ${canTest && !this._testing
            ? `<button class="btn btn-secondary" id="pv-btn-test">${testBtnLabel}</button>`
            : ''}
        </div>
      </div>

      ${acceptRejectHtml}
    `;

    document.getElementById('pv-btn-test')?.addEventListener('click', () =>
      this._startCorpusTest(p.id));
    document.getElementById('pv-btn-accept')?.addEventListener('click', () =>
      this._acceptProposal(p.id));
    document.getElementById('pv-btn-reject')?.addEventListener('click', () =>
      this._rejectProposal(p.id));
  }

  _dealRefHtml(ref) {
    const imp = fmtImp(ref.imp_margin || 0);
    return /* html */`
      <div class="deal-ref-row">
        <div class="deal-ref-imp ${imp.cls}">${imp.str} IMP</div>
        <div class="deal-ref-meta">
          Board ${ref.board || '—'} &nbsp;·&nbsp;
          Dlr ${ref.dealer || '—'} &nbsp;·&nbsp;
          Vul ${ref.vul || '—'}
        </div>
      </div>`;
  }

  // -------------------------------------------------------------------------
  // Corpus test (WebSocket)
  // -------------------------------------------------------------------------

  _startCorpusTest(proposalId) {
    this._closeTestWs();
    this._testing = true;
    this.testProgress = { board: 0, total: 12000, changed: 0, delta_imps: 0 };

    const area = document.getElementById('pv-test-area');
    if (!area) return;

    area.innerHTML = /* html */`
      <div class="status-badge testing" style="margin-bottom:12px">Testing…</div>
      <div class="corpus-progress-wrap">
        <div class="progress-track">
          <div class="progress-fill" id="pv-prog-fill" style="width:0%"></div>
        </div>
        <div class="corpus-stat-row" id="pv-prog-stats">
          <span><span class="corpus-stat-num" id="pv-stat-board">0</span> / <span id="pv-stat-total">12,000</span></span>
          <span>Changed: <span class="corpus-stat-num" id="pv-stat-changed">0</span></span>
          <span>Δ IMP: <span class="corpus-stat-num" id="pv-stat-imp">0.00</span></span>
        </div>
      </div>
      <button class="btn btn-secondary btn-sm" id="pv-btn-stop-test">Stop</button>
    `;

    document.getElementById('pv-btn-stop-test')?.addEventListener('click', () => {
      this._closeTestWs();
      this._testing = false;
      // Refresh the proposal detail to reset test area
      if (this.selectedProposal) this._renderProposalDetail(this.selectedProposal);
    });

    const url = wsUrl(`/ws/proposals/${proposalId}/test`);
    this.testWs = new WebSocket(url);

    this.testWs.addEventListener('message', e => {
      let msg;
      try { msg = JSON.parse(e.data); } catch { return; }

      if (msg.type === 'progress') {
        this._updateTestProgress(msg);
      } else if (msg.type === 'result') {
        this._onTestResult(msg);
      }
    });

    this.testWs.addEventListener('error', () => {
      area.innerHTML += `<div class="error-banner mt-8">WebSocket error during test.</div>`;
      this._testing = false;
    });

    this.testWs.addEventListener('close', () => {
      this._testing = false;
    });
  }

  _updateTestProgress(msg) {
    const total   = msg.total   || 12000;
    const board   = msg.board   || 0;
    const changed = msg.changed || 0;
    const delta   = msg.delta_imps ?? 0;
    const pct     = Math.min(100, Math.round((board / total) * 100));

    const fill = document.getElementById('pv-prog-fill');
    if (fill) fill.style.width = `${pct}%`;

    const set = (id, val) => {
      const el = document.getElementById(id);
      if (el) el.textContent = val;
    };

    set('pv-stat-board',   board.toLocaleString());
    set('pv-stat-total',   total.toLocaleString());
    set('pv-stat-changed', changed.toLocaleString());
    set('pv-stat-imp',     (delta >= 0 ? '+' : '') + delta.toFixed(3));
  }

  _onTestResult(result) {
    this._closeTestWs();
    this._testing = false;

    // Merge result into selected proposal so re-render shows it
    if (this.selectedProposal) {
      this.selectedProposal.test_result = result;
      this.selectedProposal.status = result.status || this.selectedProposal.status;
    }

    const area = document.getElementById('pv-test-area');
    if (!area) return;
    area.innerHTML = this._buildResultHtml(result);

    area.querySelector('#pv-btn-accept-result')?.addEventListener('click', () =>
      this._acceptProposal(this.selectedProposal?.id));
    area.querySelector('#pv-btn-reject-result')?.addEventListener('click', () =>
      this._rejectProposal(this.selectedProposal?.id));
  }

  _buildResultHtml(result) {
    const verdict = (result.verdict || 'INCONCLUSIVE').toUpperCase();
    const verdictCls =
      verdict === 'SHIP'          ? 'verdict-ship'
      : verdict === 'REVERT'      ? 'verdict-revert'
      : 'verdict-inconclusive';

    const meanDelta = result.mean_imp_delta ?? 0;
    const changed   = result.boards_changed ?? 0;
    const total     = result.total_boards ?? 12000;
    const tStat     = result.t_stat ?? 0;
    const pVal      = result.p_value ?? 1;

    const statCards = [
      ['Mean Δ IMP / board', (meanDelta >= 0 ? '+' : '') + meanDelta.toFixed(3)],
      ['Boards changed',     `${changed.toLocaleString()} / ${total.toLocaleString()}`],
      ['t-statistic',        tStat.toFixed(3)],
      ['p-value',            pVal.toFixed(4)],
    ].map(([lbl, val]) => /* html */`
      <div class="result-stat">
        <div class="result-stat-label">${lbl}</div>
        <div class="result-stat-value">${val}</div>
      </div>`).join('');

    const distHtml = this._buildDistChart(result.imp_distribution || []);

    const changedRows = (result.changed_boards || []).slice(0, 20).map(b => /* html */`
      <tr>
        <td>${b.board ?? '—'}</td>
        <td>${b.dealer ?? '—'}</td>
        <td>${b.vul ?? '—'}</td>
        <td>${b.old_score ?? '—'}</td>
        <td>${b.new_score ?? '—'}</td>
        <td style="color:${(b.imp_delta||0) >= 0 ? 'var(--accent)' : 'var(--red)'}">${
          (b.imp_delta ?? 0) >= 0 ? '+' : ''}${b.imp_delta ?? '—'
        }</td>
      </tr>`).join('');

    return /* html */`
      <div class="verdict-block">
        <div class="verdict-eyebrow">Test Verdict</div>
        <div class="verdict-text ${verdictCls}">${verdict}</div>
      </div>

      <div class="result-grid">${statCards}</div>

      ${distHtml ? /* html */`
      <div class="imp-dist-wrap">
        <div class="imp-dist-title">IMP Δ Distribution</div>
        ${distHtml}
      </div>` : ''}

      ${changedRows ? /* html */`
      <div class="proposal-section-label">Changed Boards (first 20)</div>
      <div class="table-overflow">
        <table class="changed-tbl">
          <thead>
            <tr>
              <th>Board</th><th>Dlr</th><th>Vul</th>
              <th>Old NS</th><th>New NS</th><th>Δ IMP</th>
            </tr>
          </thead>
          <tbody>${changedRows}</tbody>
        </table>
      </div>` : ''}

      <div class="result-actions">
        <button class="btn btn-primary"  id="pv-btn-accept-result">Accept</button>
        <button class="btn btn-danger"   id="pv-btn-reject-result">Reject</button>
      </div>
    `;
  }

  /**
   * Build a simple DIV-based horizontal bar chart from distribution data.
   * Expected: [{bucket: "≤−10", count: 45}, ...]
   * Also handles a raw array of IMP deltas (numbers), which we bucket.
   */
  _buildDistChart(raw) {
    if (!raw || raw.length === 0) return '';

    let buckets;

    if (typeof raw[0] === 'number') {
      // Raw IMP array — bucket into ranges
      const bins = {
        '≤−10': 0, '−9 to −6': 0, '−5 to −3': 0, '−2 to −1': 0,
        '0': 0,
        '+1 to +2': 0, '+3 to +5': 0, '+6 to +9': 0, '≥+10': 0,
      };
      for (const v of raw) {
        if      (v <= -10) bins['≤−10']++;
        else if (v <= -6)  bins['−9 to −6']++;
        else if (v <= -3)  bins['−5 to −3']++;
        else if (v <= -1)  bins['−2 to −1']++;
        else if (v === 0)  bins['0']++;
        else if (v <= 2)   bins['+1 to +2']++;
        else if (v <= 5)   bins['+3 to +5']++;
        else if (v <= 9)   bins['+6 to +9']++;
        else               bins['≥+10']++;
      }
      buckets = Object.entries(bins).map(([bucket, count]) => ({ bucket, count }));
    } else {
      buckets = raw;
    }

    const maxCount = Math.max(...buckets.map(b => b.count || 0), 1);

    return buckets.map(b => {
      const count = b.count || 0;
      const label = b.bucket || '?';
      const pct   = Math.round((count / maxCount) * 100);
      const neg   = label.startsWith('−') || label.startsWith('≤−') || label.includes('to −');
      const zer   = label === '0';
      const cls   = zer ? 'zer' : neg ? 'neg' : 'pos';
      return /* html */`
        <div class="imp-dist-row">
          <div class="imp-dist-lbl">${label}</div>
          <div class="imp-dist-track">
            <div class="imp-dist-bar ${cls}" style="width:${pct}%"></div>
          </div>
          <div class="imp-dist-cnt">${count}</div>
        </div>`;
    }).join('');
  }

  // -------------------------------------------------------------------------
  // Accept / Reject
  // -------------------------------------------------------------------------

  async _acceptProposal(id) {
    if (!id) return;
    try {
      await apiFetch(`/api/proposals/${id}/accept`, { method: 'POST' });
      this._onStatusChange(id, 'accepted');
    } catch (err) {
      alert(`Error: ${err.message}`);
    }
  }

  async _rejectProposal(id) {
    if (!id) return;
    try {
      await apiFetch(`/api/proposals/${id}/reject`, { method: 'POST' });
      this._onStatusChange(id, 'rejected');
    } catch (err) {
      alert(`Error: ${err.message}`);
    }
  }

  _onStatusChange(id, status) {
    // Update in-memory list
    const p = this.proposals.find(x => x.id === id);
    if (p) p.status = status;

    if (this.selectedProposal?.id === id) {
      this.selectedProposal.status = status;
      this._renderProposalDetail(this.selectedProposal);
    }

    // Refresh sidebar card badge
    const card = document.getElementById(`pcard-${id}`);
    if (card) {
      const badge = card.querySelector('.status-badge');
      if (badge) {
        badge.className = `status-badge ${statusClass(status)}`;
        badge.textContent = status;
      }
    }
  }

  // -------------------------------------------------------------------------
  // Helpers
  // -------------------------------------------------------------------------

  _closeTestWs() {
    if (this.testWs) {
      this.testWs.close();
      this.testWs = null;
    }
    this._testing = false;
  }

  /** Escape HTML entities to prevent injection */
  _esc(str) {
    return String(str ?? '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }
}
