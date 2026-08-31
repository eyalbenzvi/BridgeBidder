/**
 * deal-view.js — Deal Explorer
 *
 * Generates bridge deals until BEN beats our engine, then lets the
 * user inspect each bid, edit bidding rules, and queue staged patches
 * for submission as a proposal.
 */

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

const SEATS = ['W', 'N', 'E', 'S'];

/** Seat name → column index in the W/N/E/S auction grid */
const SEAT_COL = { W: 0, N: 1, E: 2, S: 3 };

/** Suit order and display meta */
const SUITS = [
  { key: 's', sym: '♠', cls: 's', label: '♠' },
  { key: 'h', sym: '♥', cls: 'h', label: '♥' },
  { key: 'd', sym: '♦', cls: 'd', label: '♦' },
  { key: 'c', sym: '♣', cls: 'c', label: '♣' },
];

/** Convert hand string "AQ52.K94.T3.KJ76" → {s, h, d, c} rank strings */
function parseHand(handStr) {
  const [s, h, d, c] = handStr.split('.');
  return { s, h, d, c };
}

/** Display a rank string: T → 10, space-separated */
function fmtRanks(ranks) {
  if (!ranks) return '—';
  return ranks.split('').map(r => r === 'T' ? '10' : r).join(' ') || '—';
}

/** Format date in Israeli locale */
function fmtDate(iso) {
  return new Date(iso).toLocaleDateString('he-IL', {
    year: 'numeric', month: '2-digit', day: '2-digit',
  });
}

/** Build a WebSocket URL relative to the current page */
function wsUrl(path) {
  const proto = location.protocol === 'https:' ? 'wss:' : 'ws:';
  return `${proto}//${location.host}${path}`;
}

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

/** Vulnerability → pill CSS class */
function vulClass(vul) {
  const map = { NS: 'ns', EW: 'ew', Both: 'both', None: 'none' };
  return `vul-pill vul-${map[vul] || 'none'}`;
}

/** IMP → signed string, CSS class */
function fmtImp(n) {
  const abs = Math.abs(n);
  const sign = n > 0 ? '+' : n < 0 ? '−' : '';
  return { str: `${sign}${abs}`, cls: n > 0 ? 'pos' : n < 0 ? 'neg' : 'zero' };
}

/** Build compact text summary of a patch */
function patchSummary(patch) {
  switch (patch.type) {
    case 'modify_rule': {
      const fields = Object.keys(patch.changes || {}).join(', ');
      return `Modified ${patch.rule_id}: ${fields}`;
    }
    case 'add_exception':
      return `Exception added to ${patch.rule_id}`;
    case 'add_rule':
      return `New rule added to ${patch.context_id}`;
    default:
      return JSON.stringify(patch);
  }
}

// ---------------------------------------------------------------------------
// Class
// ---------------------------------------------------------------------------

export class DealView {
  constructor(root) {
    this.root = root;
    /** @type {WebSocket|null} */
    this.ws = null;
    /** @type {object|null} */
    this.currentDeal = null;
    /** @type {{table:string,call_n:number}|null} */
    this.selectedBid = null;
    /** @type {object|null} */
    this.lastExplanation = null;
    /** @type {Array<object>} — persisted to localStorage */
    this.stagedPatches = this._loadPatches();
    /** @type {boolean} */
    this._generating = false;
  }

  // -------------------------------------------------------------------------
  // Lifecycle
  // -------------------------------------------------------------------------

  render() {
    this.root.innerHTML = this._tpl();
    this._bindStaticEvents();
    this._renderStagedPatchList();
  }

  destroy() {
    this._stopWs();
  }

  // -------------------------------------------------------------------------
  // Template
  // -------------------------------------------------------------------------

  _tpl() {
    return /* html */`
<div class="deal-view">
  <!-- Generation bar -->
  <div class="gen-bar" id="dv-gen-bar">
    <div class="gen-bar-inner">
      <div class="gen-status">
        <span class="gen-dot" id="dv-gen-dot"></span>
        <span id="dv-gen-text">Ready to find a deal.</span>
        <span class="gen-counter" id="dv-gen-counter"></span>
      </div>
      <div class="gen-actions">
        <button class="btn btn-felt btn-sm" id="dv-btn-find">Find Deal</button>
        <button class="btn btn-secondary btn-sm hidden" id="dv-btn-stop">Stop</button>
      </div>
    </div>
  </div>

  <!-- Two-panel body -->
  <div class="two-panel">

    <!-- Left / main panel -->
    <div class="main-panel" id="dv-main">

      <!-- Empty state (shown when no deal) -->
      <div id="dv-empty" class="deal-empty">
        <div class="deal-empty-suits">
          <span class="s">♠</span><span class="h">♥</span><span class="d">♦</span><span class="c">♣</span>
        </div>
        <p class="deal-empty-tagline">Find a deal where BEN's bidding outscores your engine.</p>
        <button class="btn btn-primary" id="dv-btn-find-2">Find Deal</button>
      </div>

      <!-- Deal content (hidden until deal found) -->
      <div id="dv-content" class="hidden">
        <div id="dv-header" class="deal-header"></div>
        <div id="dv-compass" class="compass-wrap"></div>
        <div id="dv-auction" class="auction-duo"></div>
        <div id="dv-score"  class="score-bar"></div>
        <div id="dv-footer" class="action-footer"></div>
      </div>

      <!-- Error banner (hidden by default) -->
      <div id="dv-error" class="error-banner hidden"></div>
    </div>

    <!-- Right / inspector panel -->
    <aside class="inspector-panel hidden" id="dv-inspector">
      <!-- Populated by _renderInspector() -->
    </aside>

  </div>
</div>
`;
  }

  // -------------------------------------------------------------------------
  // Static event bindings
  // -------------------------------------------------------------------------

  _bindStaticEvents() {
    document.getElementById('dv-btn-find').addEventListener('click', () => this.startGeneration());
    document.getElementById('dv-btn-find-2').addEventListener('click', () => this.startGeneration());
    document.getElementById('dv-btn-stop').addEventListener('click', () => this.stopGeneration());
  }

  // -------------------------------------------------------------------------
  // Generation
  // -------------------------------------------------------------------------

  startGeneration() {
    if (this._generating) return;
    this._generating = true;

    // Reset deal UI
    this.currentDeal = null;
    this.selectedBid = null;
    this.lastExplanation = null;
    document.getElementById('dv-content').classList.add('hidden');
    document.getElementById('dv-empty').classList.add('hidden');
    document.getElementById('dv-error').classList.add('hidden');
    this._hideInspector();

    // Update gen bar
    const dot = document.getElementById('dv-gen-dot');
    dot.classList.add('pulsing');
    document.getElementById('dv-gen-text').textContent = 'Searching for a deal where BEN wins…';
    document.getElementById('dv-gen-counter').textContent = '0 tried';
    document.getElementById('dv-btn-find').classList.add('hidden');
    document.getElementById('dv-btn-stop').classList.remove('hidden');

    const seed = Math.floor(Math.random() * 1_000_000);
    const url  = wsUrl(`/ws/deals/generate?seed=${seed}`);

    this.ws = new WebSocket(url);

    this.ws.addEventListener('message', e => {
      let msg;
      try { msg = JSON.parse(e.data); } catch { return; }

      if (msg.type === 'progress') {
        const n = msg.tried || 0;
        document.getElementById('dv-gen-counter').textContent =
          `${n.toLocaleString()} tried`;
      } else if (msg.type === 'source') {
        this._source = msg.source;
        if (msg.source === 'corpus') {
          document.getElementById('dv-gen-text').textContent =
            `Drawing from ${(msg.pool_size || 0).toLocaleString()} boards BEN already won…`;
        }
      } else if (msg.type === 'found') {
        this._onDealFound(msg.deal);
      } else if (msg.type === 'error') {
        this._showError(msg.message || 'Could not produce a deal.');
        this._resetGenBar();
      }
    });

    this.ws.addEventListener('error', () => {
      this._showError('WebSocket error — is the server running?');
      this._resetGenBar();
    });

    this.ws.addEventListener('close', () => {
      if (this._generating && !this.currentDeal) {
        // Closed before finding a deal and user didn't stop
      }
      this._generating = false;
    });
  }

  stopGeneration() {
    this._stopWs();
    this._resetGenBar();
    if (!this.currentDeal) {
      document.getElementById('dv-empty').classList.remove('hidden');
    }
  }

  _stopWs() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    this._generating = false;
  }

  _resetGenBar() {
    document.getElementById('dv-gen-dot').classList.remove('pulsing');
    document.getElementById('dv-btn-find').classList.remove('hidden');
    document.getElementById('dv-btn-stop').classList.add('hidden');
    this._generating = false;
  }

  // -------------------------------------------------------------------------
  // Deal found
  // -------------------------------------------------------------------------

  _onDealFound(deal) {
    this._stopWs();
    this.currentDeal = deal;

    // Update gen bar to show summary
    const imp = fmtImp(deal.imp_margin);
    document.getElementById('dv-gen-dot').classList.remove('pulsing');
    // Two sources, and the label says which: a board played just now against
    // the live model, or one replayed from the pool where BEN already won it.
    // Both are real losses; only one is news.
    document.getElementById('dv-gen-text').textContent =
      deal.source === 'corpus'
        ? `Board ${deal.board} from ${deal.source_file || 'the pool'} — BEN won by ${imp.str} IMP`
        : `Found after ${(deal.tried || 0).toLocaleString()} deals — BEN won by ${imp.str} IMP`;
    document.getElementById('dv-gen-counter').textContent = '';
    document.getElementById('dv-btn-stop').classList.add('hidden');
    document.getElementById('dv-btn-find').classList.remove('hidden');
    document.getElementById('dv-btn-find').textContent = 'Find Another';

    // Render deal content
    this._renderDealHeader(deal);
    this._renderCompass(deal.hands, deal.dealer, deal.vul);
    this._renderAuctionDuo(deal);
    this._renderScoreBar(deal);
    this._renderActionFooter(deal);

    document.getElementById('dv-empty').classList.add('hidden');
    document.getElementById('dv-content').classList.remove('hidden');
  }

  // -------------------------------------------------------------------------
  // Deal header
  // -------------------------------------------------------------------------

  _renderDealHeader(deal) {
    const imp  = fmtImp(deal.imp_margin);
    const el   = document.getElementById('dv-header');
    el.innerHTML = /* html */`
      <div class="deal-board">Board ${deal.board}</div>
      <div class="deal-meta-item">
        <span class="deal-meta-label">Dlr</span>
        <span class="deal-meta-value">${deal.dealer}</span>
      </div>
      <div class="deal-meta-item">
        <span class="deal-meta-label">Vul</span>
        <span class="${vulClass(deal.vul)}">${deal.vul}</span>
      </div>
      <div class="deal-tried-note">${
        deal.source === 'corpus'
          ? `From the pool · ${deal.source_file || ''}`
          : `Found after ${(deal.tried || 0).toLocaleString()} deals`
      }</div>
      ${(deal.drift && deal.drift.length) ? /* html */`
      <div class="drift-banner" title="${deal.drift.join('\n')}">
        ⚠ The system has changed since this board was recorded — the engine now
        bids differently at ${deal.drift.length} position${
          deal.drift.length === 1 ? '' : 's'}.
      </div>` : ''}
    `;
  }

  // -------------------------------------------------------------------------
  // Compass diagram
  // -------------------------------------------------------------------------

  _renderCompass(hands, dealer, vul) {
    const wrap = document.getElementById('dv-compass');
    const handHtml = (seat) => {
      const h   = parseHand(hands[seat] || '...');
      const dlr = seat === dealer ? '<span class="dlr-badge">Dlr</span>' : '';
      const rows = SUITS.map(s => /* html */`
        <div class="suit-row">
          <span class="suit-sym ${s.cls}">${s.sym}</span>
          <span class="suit-cards">${fmtRanks(h[s.key])}</span>
        </div>`).join('');
      return /* html */`
        <div class="compass-hand compass-hand-${seat.toLowerCase()}">
          <div class="hand-seat-row">
            <span class="hand-seat">${seat}</span>${dlr}
          </div>
          <div class="hand-suits">${rows}</div>
        </div>`;
    };

    wrap.innerHTML = /* html */`
      <div class="compass">
        <div class="compass-empty"></div>
        ${handHtml('N')}
        <div class="compass-empty"></div>
        ${handHtml('W')}
        <div class="compass-center">N</div>
        ${handHtml('E')}
        <div class="compass-empty"></div>
        ${handHtml('S')}
        <div class="compass-empty"></div>
      </div>`;
  }

  // -------------------------------------------------------------------------
  // Auction tables
  // -------------------------------------------------------------------------

  _renderAuctionDuo(deal) {
    const wrap = document.getElementById('dv-auction');
    wrap.innerHTML = '';
    wrap.appendChild(this._buildAuctionTable(deal.table_a, 'Table A', 'a', deal.dealer));
    wrap.appendChild(this._buildAuctionTable(deal.table_b, 'Table B', 'b', deal.dealer));
  }

  /**
   * Build one auction table (for table_a or table_b).
   * Seats always appear as W / N / E / S (left → right).
   * Empty cells pad the first row before the dealer column.
   */
  _buildAuctionTable(tableData, label, tableKey, dealer) {
    const dealerIdx = SEAT_COL[dealer] ?? 0;
    const ourSeats  = (tableData.our_side || '').split('');

    // Assign each auction call to a seat, and find call_n for our calls
    let ourN = 0;
    const cells = tableData.auction.map((call, i) => {
      const seatIdx = (dealerIdx + i) % 4;
      const seat    = SEATS[seatIdx];
      const isOurs  = ourSeats.includes(seat);
      const callN   = isOurs ? ourN++ : null;
      return { call, seat, seatIdx, isOurs, callN };
    });

    // Build table rows
    const totalCells = dealerIdx + cells.length;
    const rows       = Math.ceil(totalCells / 4);
    let rowsHtml     = '';

    for (let r = 0; r < rows; r++) {
      let tds = '';
      for (let col = 0; col < 4; col++) {
        const pos = r * 4 + col;
        if (pos < dealerIdx) {
          tds += `<td class="empty"></td>`;
          continue;
        }
        const idx = pos - dealerIdx;
        if (idx >= cells.length) {
          tds += `<td></td>`;
          continue;
        }
        const cell = cells[idx];
        tds += this._buildBidCell(cell, tableKey);
      }
      rowsHtml += `<tr>${tds}</tr>`;
    }

    const ourSideChip = tableData.our_side
      ? `<span class="our-side-chip">${tableData.our_side}</span>`
      : '';

    const wrap = document.createElement('div');
    wrap.className = 'auction-table-wrap';
    wrap.innerHTML = /* html */`
      <div class="auction-table-label">${label} ${ourSideChip}</div>
      <table class="auction-tbl">
        <thead>
          <tr>
            <th>W</th><th>N</th><th>E</th><th>S</th>
          </tr>
        </thead>
        <tbody>${rowsHtml}</tbody>
      </table>`;

    // Event delegation for engine bids
    wrap.querySelector('tbody').addEventListener('click', e => {
      const td = e.target.closest('td.engine-bid');
      if (!td) return;
      const cn = parseInt(td.dataset.callN, 10);
      this._onBidClick(tableKey, cn, td);
    });

    return wrap;
  }

  _buildBidCell(cell, tableKey) {
    const call = cell.call;
    if (!call) return `<td></td>`;

    let cls  = '';
    let text = call;

    if (call === 'P' || call === 'Pass') { cls = 'bid-p'; text = 'P'; }
    else if (call === 'X' || call === 'Dbl')  { cls = 'bid-x'; text = 'X'; }
    else if (call === 'XX' || call === 'Rdbl') { cls = 'bid-xx'; text = 'XX'; }

    if (cell.isOurs) {
      cls += ' engine-bid';
      const id = `bid-${tableKey}-${cell.callN}`;
      return /* html */`<td
        class="${cls.trim()}"
        data-table="${tableKey}"
        data-call-n="${cell.callN}"
        id="${id}"
        tabindex="0"
        title="Click to inspect (${cell.seat})"
      >${text}</td>`;
    }

    return `<td class="${cls.trim()}">${text}</td>`;
  }

  // -------------------------------------------------------------------------
  // Score bar
  // -------------------------------------------------------------------------

  _renderScoreBar(deal) {
    const ta  = deal.table_a;
    const tb  = deal.table_b;
    const imp = fmtImp(deal.imp_margin);
    const el  = document.getElementById('dv-score');
    el.innerHTML = /* html */`
      <div class="score-section">
        <div class="score-section-label">Table A — ${ta.our_side}</div>
        <div class="score-section-value">${ta.score_ns >= 0 ? '+' : ''}${ta.score_ns}</div>
        <div class="score-section-contract">${ta.contract} · ${ta.tricks} tricks</div>
      </div>
      <div class="score-imp">
        <div class="imp-number ${imp.cls}">${imp.str}</div>
        <div class="imp-unit">IMP</div>
      </div>
      <div class="score-section">
        <div class="score-section-label">Table B — ${tb.our_side}</div>
        <div class="score-section-value">${tb.score_ns >= 0 ? '+' : ''}${tb.score_ns}</div>
        <div class="score-section-contract">${tb.contract} · ${tb.tricks} tricks</div>
      </div>`;
  }

  // -------------------------------------------------------------------------
  // Action footer
  // -------------------------------------------------------------------------

  _renderActionFooter(deal) {
    const el = document.getElementById('dv-footer');
    el.innerHTML = /* html */`
      <button class="btn btn-secondary" id="dv-btn-next">Next Deal</button>
      <button class="btn btn-primary"   id="dv-btn-submit">Submit Proposal</button>`;
    document.getElementById('dv-btn-next').addEventListener('click', () => this.nextDeal());
    document.getElementById('dv-btn-submit').addEventListener('click', () => this._openSubmitModal());
  }

  // -------------------------------------------------------------------------
  // Bid click → inspector
  // -------------------------------------------------------------------------

  async _onBidClick(table, callN, td) {
    if (!this.currentDeal) return;

    // Mark selected cell
    document.querySelectorAll('.engine-bid.selected').forEach(el => el.classList.remove('selected'));
    td.classList.add('selected');
    this.selectedBid = { table, call_n: callN };

    const inspector = document.getElementById('dv-inspector');
    inspector.classList.remove('hidden');
    inspector.innerHTML = /* html */`
      <div class="inspector-header">
        <div class="inspector-rule-id">Loading…</div>
        <div class="inspector-call-row">
          <span class="inspector-call">…</span>
        </div>
      </div>`;

    try {
      const expl = await apiFetch(
        `/api/deals/${this.currentDeal.id}/explain/${table}/${callN}`
      );
      this.lastExplanation = expl;
      this._renderInspector(expl);
    } catch (err) {
      inspector.innerHTML = /* html */`
        <div class="inspector-header" style="background:var(--felt)">
          <div class="inspector-rule-id">Error</div>
        </div>
        <div class="inspector-body">
          <div class="inspector-section">
            <div class="error-banner" style="margin:0">${err.message}</div>
          </div>
        </div>`;
    }
  }

  _hideInspector() {
    document.getElementById('dv-inspector').classList.add('hidden');
    document.querySelectorAll('.engine-bid.selected').forEach(el => el.classList.remove('selected'));
  }

  // -------------------------------------------------------------------------
  // Inspector rendering
  // -------------------------------------------------------------------------

  _renderInspector(expl) {
    const inspector = document.getElementById('dv-inspector');

    // Constraint pills
    const c = expl.constraint || {};
    const pills = [];
    if (c.hcp) pills.push(`HCP ${c.hcp[0]}–${c.hcp[1]}`);
    const lengths = c.lengths || c.suits || {};
    for (const [suit, rng] of Object.entries(lengths)) {
      if (Array.isArray(rng)) pills.push(`${suit.toUpperCase()} ${rng[0]}–${rng[1]}`);
    }
    const pillsHtml = pills.map(p => `<span class="cpill">${p}</span>`).join('');

    // Denies
    const deniesHtml = (expl.denies || []).map(d =>
      `<div class="denies-item">${d.text || JSON.stringify(d)}</div>`
    ).join('');

    // Fit bar
    const fitPct = Math.round((expl.fit_score || 0) * 100);

    // Candidates
    const cands = expl.candidates || [];
    const candRows = cands.map((cand, i) => {
      const fitW = Math.round((cand.fit || 0) * 100);
      const scoreW = Math.round((cand.score || 0) * 100);
      return /* html */`
        <tr class="${i === 0 ? 'cand-best' : ''}">
          <td>${cand.call || '—'}</td>
          <td class="mini-bar-cell">
            <div class="mini-bar-wrap">
              <div class="mini-bar-track"><div class="mini-bar-fill" style="width:${fitW}%"></div></div>
              <span>${fitW}%</span>
            </div>
          </td>
          <td>${cand.rule || '—'}</td>
          <td>${scoreW}%</td>
          <td>${cand.priority || '—'}</td>
        </tr>`;
    }).join('');

    inspector.innerHTML = /* html */`
      <div class="inspector-header">
        <div class="inspector-rule-id">${expl.rule_id || '—'}</div>
        <div class="inspector-call-row">
          <span class="inspector-call">${expl.call || '—'}</span>
          <span class="priority-badge">P${expl.priority || '—'}</span>
        </div>
      </div>

      <div class="inspector-body">
        <div class="inspector-section">
          <div class="section-label">Context</div>
          <div class="context-chip">
            <span>${expl.context_id || '—'}</span>
            <span style="opacity:0.55">${expl.context_pattern || ''}</span>
          </div>
        </div>

        <div class="inspector-section">
          <div class="section-label">Shows</div>
          <div class="shows-block">
            <div class="shows-text">${expl.shows || '—'}</div>
            ${pillsHtml ? `<div class="constraint-pills">${pillsHtml}</div>` : ''}
            ${expl.forcing_status ? `<div class="mt-8" style="font-size:0.72rem;color:var(--text-sub)">${expl.forcing_status.replace(/_/g,' ')}</div>` : ''}
            <div class="fit-row">
              <span>Fit</span>
              <div class="fit-track"><div class="fit-fill" style="width:${fitPct}%"></div></div>
              <span>${fitPct}%</span>
            </div>
          </div>
          ${deniesHtml ? `<div class="denies-list mt-8">${deniesHtml}</div>` : ''}
        </div>

        ${candRows ? /* html */`
        <div class="inspector-section">
          <div class="section-label">Candidates</div>
          <table class="cand-table">
            <thead>
              <tr>
                <th>Call</th><th>Fit</th><th>Rule</th><th>Score</th><th>Pri</th>
              </tr>
            </thead>
            <tbody>${candRows}</tbody>
          </table>
        </div>` : ''}

        <!-- Rule editor accordion -->
        <div class="rule-editor-accordion" id="dv-editor-accordion">
          <button class="rule-editor-toggle"
                  aria-expanded="false"
                  id="dv-editor-toggle"
          >
            Edit Rule
            <span class="toggle-arrow">▼</span>
          </button>
          <div id="dv-editor-form-wrap" class="hidden">
            ${this._buildEditorFormHtml(expl)}
          </div>
        </div>

        <!-- Staged patches -->
        <div class="staged-patches-section" id="dv-staged-section">
          ${this._stagedPatchesHtml()}
        </div>
      </div>`;

    // Accordion toggle
    document.getElementById('dv-editor-toggle').addEventListener('click', e => {
      const btn  = e.currentTarget;
      const wrap = document.getElementById('dv-editor-form-wrap');
      const open = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', String(!open));
      wrap.classList.toggle('hidden', open);
    });

    // Editor form events
    this._bindEditorFormEvents(expl);
  }

  // -------------------------------------------------------------------------
  // Rule editor form
  // -------------------------------------------------------------------------

  _buildEditorFormHtml(expl) {
    const c     = expl.constraint || {};
    const hcp   = c.hcp || [0, 37];
    const lengths = c.lengths || c.suits || {};
    const defLen = (suit) => {
      const v = lengths[suit.toLowerCase()] || lengths[suit.toUpperCase()];
      return Array.isArray(v) ? v : [0, 13];
    };

    const suitCols = ['S', 'H', 'D', 'C'].map(suit => /* html */`
      <div class="suit-col">
        <div class="suit-col-header">
          <span class="suit-sym ${suit.toLowerCase()}">${{S:'♠',H:'♥',D:'♦',C:'♣'}[suit]}</span>
        </div>
        <input class="form-input" type="number" min="0" max="13"
               id="ed-len-${suit.toLowerCase()}-min"
               value="${defLen(suit)[0]}" placeholder="min">
        <input class="form-input" type="number" min="0" max="13"
               id="ed-len-${suit.toLowerCase()}-max"
               value="${defLen(suit)[1]}" placeholder="max">
      </div>`).join('');

    const forcingOptions = [
      ['non_forcing',   'Non-forcing'],
      ['forcing',       'Forcing'],
      ['game_forcing',  'Game-forcing'],
      ['passable',      'Passable'],
    ].map(([val, lbl]) =>
      `<option value="${val}" ${expl.forcing_status === val ? 'selected' : ''}>${lbl}</option>`
    ).join('');

    return /* html */`
      <div class="rule-editor-form">

        <div class="form-field">
          <label class="form-field-label">HCP range</label>
          <div class="range-row">
            <input class="form-input" type="number" min="0" max="37"
                   id="ed-hcp-min" value="${hcp[0]}">
            <span class="range-sep">–</span>
            <input class="form-input" type="number" min="0" max="37"
                   id="ed-hcp-max" value="${hcp[1]}">
          </div>
        </div>

        <div class="form-field">
          <label class="form-field-label">Suit lengths (min / max)</label>
          <div class="suit-grid">${suitCols}</div>
        </div>

        <div class="form-field">
          <label class="form-field-label" for="ed-priority">Priority</label>
          <div class="priority-row">
            <input class="priority-slider" type="range"
                   id="ed-priority" min="1" max="100"
                   value="${expl.priority || 50}">
            <span class="priority-val" id="ed-priority-val">${expl.priority || 50}</span>
          </div>
        </div>

        <div class="form-field">
          <label class="form-field-label" for="ed-shows">Shows</label>
          <input class="form-input wide" type="text"
                 id="ed-shows" value="${(expl.shows || '').replace(/"/g, '&quot;')}">
        </div>

        <div class="form-field">
          <label class="form-field-label" for="ed-forcing">Forcing status</label>
          <select class="form-select" id="ed-forcing">${forcingOptions}</select>
        </div>

        <div class="editor-actions">
          <button class="btn btn-primary btn-sm"    id="ed-btn-modify">Save Modification</button>
          <button class="btn btn-ghost btn-sm"      id="ed-btn-exception">Add Exception</button>
          <button class="btn btn-secondary btn-sm"  id="ed-btn-subrule">Add Sub-rule</button>
        </div>

      </div>`;
  }

  _bindEditorFormEvents(expl) {
    // Priority slider live display
    const slider = document.getElementById('ed-priority');
    const valEl  = document.getElementById('ed-priority-val');
    if (slider && valEl) {
      slider.addEventListener('input', () => { valEl.textContent = slider.value; });
    }

    document.getElementById('ed-btn-modify')?.addEventListener('click', () =>
      this._saveModification(expl));
    document.getElementById('ed-btn-exception')?.addEventListener('click', () =>
      this._addException(expl));
    document.getElementById('ed-btn-subrule')?.addEventListener('click', () =>
      this._addSubRule(expl));
  }

  _collectEditorForm() {
    const v = (id) => document.getElementById(id)?.value;
    const n = (id) => parseFloat(v(id));
    return {
      hcp:          [n('ed-hcp-min'), n('ed-hcp-max')],
      lengths: {
        s: [n('ed-len-s-min'), n('ed-len-s-max')],
        h: [n('ed-len-h-min'), n('ed-len-h-max')],
        d: [n('ed-len-d-min'), n('ed-len-d-max')],
        c: [n('ed-len-c-min'), n('ed-len-c-max')],
      },
      priority:       n('ed-priority'),
      shows:          v('ed-shows'),
      forcing_status: v('ed-forcing'),
    };
  }

  async _saveModification(expl) {
    const form = this._collectEditorForm();
    const original = expl.constraint || {};
    const changes = {};

    // Only record fields that changed
    if (JSON.stringify(form.hcp) !== JSON.stringify(original.hcp))
      changes.hcp = { before: original.hcp, after: form.hcp };

    if (form.shows !== expl.shows)
      changes.shows = { before: expl.shows, after: form.shows };

    if (form.forcing_status !== expl.forcing_status)
      changes.forcing_status = { before: expl.forcing_status, after: form.forcing_status };

    if (form.priority !== expl.priority)
      changes.priority = { before: expl.priority, after: form.priority };

    // Lengths
    const origLengths = original.lengths || original.suits || {};
    for (const suit of ['s','h','d','c']) {
      const ov = origLengths[suit] || [0,13];
      if (JSON.stringify(form.lengths[suit]) !== JSON.stringify(ov)) {
        changes[`length_${suit}`] = { before: ov, after: form.lengths[suit] };
      }
    }

    if (Object.keys(changes).length === 0) {
      this._showBannerInEditor('No changes detected.', 'info');
      return;
    }

    const patch = {
      type:       'modify_rule',
      rule_id:    expl.rule_id,
      context_id: expl.context_id,
      changes,
    };

    await this._previewAndStage(patch);
  }

  async _addException(expl) {
    const form  = this._collectEditorForm();
    const patch = {
      type:       'add_exception',
      rule_id:    expl.rule_id,
      context_id: expl.context_id,
      constraint: {
        hcp:     form.hcp,
        lengths: form.lengths,
      },
    };
    await this._previewAndStage(patch);
  }

  async _addSubRule(expl) {
    const form  = this._collectEditorForm();
    const patch = {
      type:       'add_rule',
      context_id: expl.context_id,
      rule: {
        call:           expl.call,
        priority:       (expl.priority || 50) + 1,
        shows:          form.shows,
        forcing_status: form.forcing_status,
        constraint: {
          hcp:     form.hcp,
          lengths: form.lengths,
        },
      },
    };
    await this._previewAndStage(patch);
  }

  async _previewAndStage(patch) {
    try {
      const result = await apiFetch('/api/rules/patch/preview', {
        method: 'POST',
        body:   JSON.stringify({ patch }),
      });

      if (!result.ok) {
        this._showBannerInEditor(`Preview error: ${result.error}`, 'error');
        return;
      }

      this.stagedPatches.push(patch);
      this._savePatches();
      this._refreshStagedSection();
      this._showBannerInEditor('Patch staged.', 'info');
    } catch (err) {
      this._showBannerInEditor(`Error: ${err.message}`, 'error');
    }
  }

  _showBannerInEditor(msg, type) {
    const cls = type === 'error' ? 'error-banner' : 'info-banner';
    // Remove previous banner
    document.querySelectorAll('.editor-tmp-banner').forEach(b => b.remove());
    const banner = document.createElement('div');
    banner.className = `${cls} editor-tmp-banner`;
    banner.textContent = msg;
    const actions = document.querySelector('.editor-actions');
    actions?.parentElement?.insertBefore(banner, actions);
    setTimeout(() => banner.remove(), 3500);
  }

  // -------------------------------------------------------------------------
  // Staged patches
  // -------------------------------------------------------------------------

  _stagedPatchesHtml() {
    const count = this.stagedPatches.length;
    const countBadge = count > 0
      ? `<span class="patch-count">${count}</span>`
      : '';

    const list = this.stagedPatches.length === 0
      ? `<div class="staged-no-patches">No staged patches yet.</div>`
      : this.stagedPatches.map((p, i) => /* html */`
          <div class="patch-item">
            <div class="patch-item-text">${patchSummary(p)}</div>
            <button class="patch-discard" data-idx="${i}" title="Discard">✕</button>
          </div>`).join('');

    return /* html */`
      <div class="staged-header">
        <span class="staged-title">Staged patches</span>
        ${countBadge}
      </div>
      <div class="patch-list">${list}</div>`;
  }

  _refreshStagedSection() {
    const sec = document.getElementById('dv-staged-section');
    if (!sec) return;
    sec.innerHTML = this._stagedPatchesHtml();
    sec.querySelectorAll('.patch-discard').forEach(btn => {
      btn.addEventListener('click', () => {
        const idx = parseInt(btn.dataset.idx, 10);
        this.stagedPatches.splice(idx, 1);
        this._savePatches();
        this._refreshStagedSection();
      });
    });
  }

  _renderStagedPatchList() {
    // Called on initial render (inspector may not be open yet, skip)
  }

  _savePatches() {
    try {
      localStorage.setItem('staged_patches', JSON.stringify(this.stagedPatches));
    } catch { /* storage unavailable */ }
  }

  _loadPatches() {
    try {
      return JSON.parse(localStorage.getItem('staged_patches') || '[]');
    } catch {
      return [];
    }
  }

  // -------------------------------------------------------------------------
  // Actions
  // -------------------------------------------------------------------------

  nextDeal() {
    // Keep staged patches, clear deal state, restart
    this.currentDeal   = null;
    this.selectedBid   = null;
    this.lastExplanation = null;
    document.getElementById('dv-content').classList.add('hidden');
    this._hideInspector();
    document.getElementById('dv-btn-find').textContent = 'Find Deal';
    this.startGeneration();
  }

  _openSubmitModal() {
    if (this.stagedPatches.length === 0) {
      alert('Stage at least one rule patch before submitting a proposal.');
      return;
    }

    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay';
    overlay.innerHTML = /* html */`
      <div class="modal-box">
        <h3 class="modal-title">Submit Proposal</h3>
        <div class="modal-form">
          <div class="form-field">
            <label class="form-field-label" for="modal-name">Proposal name</label>
            <input class="form-input wide" type="text" id="modal-name"
                   placeholder="e.g. Tighten open_1NT range">
          </div>
          <div class="form-field">
            <label class="form-field-label" for="modal-note">Note (optional)</label>
            <input class="form-input wide" type="text" id="modal-note"
                   placeholder="Brief rationale…">
          </div>
        </div>
        <div class="modal-actions">
          <button class="btn btn-secondary" id="modal-cancel">Cancel</button>
          <button class="btn btn-primary"   id="modal-submit">Submit</button>
        </div>
      </div>`;

    document.body.appendChild(overlay);

    overlay.querySelector('#modal-cancel').addEventListener('click', () => overlay.remove());
    overlay.addEventListener('click', e => { if (e.target === overlay) overlay.remove(); });

    overlay.querySelector('#modal-submit').addEventListener('click', async () => {
      const name = overlay.querySelector('#modal-name').value.trim();
      if (!name) {
        overlay.querySelector('#modal-name').focus();
        return;
      }
      const note = overlay.querySelector('#modal-note').value.trim();
      await this._submitProposal(name, note);
      overlay.remove();
    });
  }

  async _submitProposal(name, note) {
    const deal = this.currentDeal;
    const body = {
      name,
      note,
      patches: this.stagedPatches,
      deal_ref: deal ? {
        id:         deal.id,
        board:      deal.board,
        dealer:     deal.dealer,
        vul:        deal.vul,
        imp_margin: deal.imp_margin,
      } : null,
    };

    try {
      await apiFetch('/api/proposals', { method: 'POST', body: JSON.stringify(body) });
      this.stagedPatches = [];
      this._savePatches();
      this._refreshStagedSection();
      window.location.hash = '#proposals';
    } catch (err) {
      this._showError(`Failed to submit proposal: ${err.message}`);
    }
  }

  _showError(msg) {
    const el = document.getElementById('dv-error');
    if (!el) return;
    el.textContent = msg;
    el.classList.remove('hidden');
    setTimeout(() => el.classList.add('hidden'), 6000);
  }
}
