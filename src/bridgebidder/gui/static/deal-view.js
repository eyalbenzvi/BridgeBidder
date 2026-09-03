/**
 * deal-view.js — Deal Explorer
 *
 * Finds a board where BEN outscored our engine, shows both auctions, and
 * explains any of our calls: the rule that fired, what it shows and denies,
 * and every candidate it beat.
 *
 * It does not edit rules. Describing what is wrong and encoding the fix in
 * the DSL are different jobs; this captures the first as a free-text note
 * with the board attached, and the fix is made by hand in the YAML.
 */

import { toast } from './ui.js';

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
    /** @type {number|null} — open notes, for the footer */
    this.noteCount = null;
    /** @type {boolean} */
    this._generating = false;
  }

  // -------------------------------------------------------------------------
  // Lifecycle
  // -------------------------------------------------------------------------

  render() {
    this.root.innerHTML = this._tpl();
    this._bindStaticEvents();
    this._refreshNoteCount();
    // Navigating away destroys this view and constructs a new one, so
    // a board held only in the instance is gone on the way back. The payload
    // is small and self-contained, so keep it for the tab's lifetime.
    const saved = this._loadDeal();
    if (saved) this._showDeal(saved, true);
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
    this._clearDeal();
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
    this._saveDeal(deal);
    this._showDeal(deal, false);
  }

  _showDeal(deal, restored) {
    this.currentDeal = deal;

    // Update gen bar to show summary
    const imp = fmtImp(deal.imp_margin);
    document.getElementById('dv-gen-dot').classList.remove('pulsing');
    // Two sources, and the label says which: a board played just now against
    // the live model, or one replayed from the pool where BEN already won it.
    // Both are real losses; only one is news.
    const summary = deal.source === 'corpus'
      ? `Board ${deal.board} from ${deal.source_file || 'the pool'} — BEN won by ${imp.str} IMP`
      : `Found after ${(deal.tried || 0).toLocaleString()} deals — BEN won by ${imp.str} IMP`;
    document.getElementById('dv-gen-text').textContent =
      restored ? `${summary} · restored` : summary;
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

    // Which calls are ours, and what to ask the server about each, both come
    // from `our_calls` -- whose `n` is the call's index in the FULL auction,
    // the key the server stores its decision setups under.
    //
    // Numbering our calls 0,1,2... instead (an ordinal among our own calls)
    // silently asks about the wrong bid: on an auction where our side's third
    // call sits at position 4, clicking it returned the explanation for
    // position 2, and clicking position 2 asked for a position that does not
    // exist. Deriving it here at all was the mistake -- `n` is already in the
    // payload and is authoritative.
    const ourByN = new Map(
      (tableData.our_calls || []).map(c => [c.n, c]));

    const cells = tableData.auction.map((call, i) => {
      const seatIdx = (dealerIdx + i) % 4;
      const seat    = SEATS[seatIdx];
      const ours    = ourByN.get(i);
      if (ours && ours.call !== call) {
        console.warn(
          `auction/our_calls disagree at n=${i}: table shows ${call}, ` +
          `our_calls says ${ours.call}`);
      }
      return { call, seat, seatIdx, isOurs: !!ours, callN: ours ? i : null,
               rule: ours ? ours.rule : null };
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

  /**
   * Footer: a note box that does not need a bid selected.
   *
   * Not every observation is about one call — "this whole auction should have
   * stopped at 2H" belongs to the board. The per-bid box in the inspector
   * attaches the call as well; this one attaches just the board.
   */
  _renderActionFooter(deal) {
    const el = document.getElementById('dv-footer');
    if (!el) return;
    const n = this.noteCount;
    el.innerHTML = /* html */`
      <div class="note-box">
        <div class="section-label">Note about this board</div>
        <textarea class="note-input" id="dv-note-text-general" rows="3"
          placeholder="Something about the deal as a whole — click a bid instead to attach that call too"></textarea>
        <div class="footer-actions">
          <button class="btn btn-primary" id="dv-note-save-general">Save note</button>
          <button class="btn btn-secondary" id="dv-btn-next">Next Deal</button>
          <a class="btn btn-ghost" href="#notes">${
            n === null ? 'Notes' : `Notes (${n})`
          }</a>
        </div>
      </div>`;
    el.querySelector('#dv-btn-next').addEventListener('click', () => this.nextDeal());
    const btn = el.querySelector('#dv-note-save-general');
    const box = el.querySelector('#dv-note-text-general');
    btn.addEventListener('click', () => this._saveNote(box.value, null, btn));
    box.addEventListener('keydown', e => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
        this._saveNote(box.value, null, btn);
      }
    });
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
      const expl = await this._fetchExplanation(table, callN);
      this.lastExplanation = expl;
      this._renderInspector(expl);
    } catch (err) {
      const gone = String(err.message || '').startsWith('404');
      const body = gone
        ? 'The server no longer has this board loaded and could not rebuild it. '
          + 'Press Find Another for a fresh one.'
        : err.message;
      inspector.innerHTML = /* html */`
        <div class="inspector-header" style="background:var(--felt)">
          <div class="inspector-rule-id">${gone ? 'Board expired' : 'Error'}</div>
        </div>
        <div class="inspector-body">
          <div class="inspector-section">
            <div class="error-banner" style="margin:0">${body}</div>
          </div>
        </div>`;
    }
  }

  /**
   * Fetch an explanation, rebuilding the board server-side if it has aged out.
   *
   * The explain cache is in memory and bounded, and a free host restarts its
   * instance every time it idles out — so a board the page is still showing
   * can stop being explainable while the user is reading it. A pool board is
   * pure data, so rather than surfacing a 404 the client asks the server to
   * replay it under the same id and tries once more. Only once: a second 404
   * means something other than eviction.
   */
  async _fetchExplanation(table, callN) {
    const deal = this.currentDeal;
    const url = `/api/deals/${deal.id}/explain/${table}/${callN}`;
    try {
      return await apiFetch(url);
    } catch (err) {
      const gone = String(err.message || '').startsWith('404');
      if (!gone || deal.source !== 'corpus' || !deal.source_file) throw err;
      await apiFetch(`/api/deals/${deal.id}/rehydrate`, {
        method: 'POST',
        body: JSON.stringify({ source_file: deal.source_file, board: deal.board }),
      });
      return await apiFetch(url);
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

        <!-- Note about this call -->
        <div class="note-box" id="dv-note-box">
          <div class="section-label">What is wrong here?</div>
          <p class="note-hint">
            Describe it however you like — the rule that should apply, the
            exception it is missing, a rule that should not exist, two rules
            fighting. The board and this bid are attached automatically.
          </p>
          <textarea class="note-input" id="dv-note-text" rows="4"
            placeholder="e.g. with 5-4 in the majors and 11 points this should be a negative double, not 1S — the rule never considers the second suit"></textarea>
          <button class="btn btn-primary btn-sm" id="dv-note-save">Save note</button>
        </div>
      </div>`;

    const save = document.getElementById('dv-note-save');
    const text = document.getElementById('dv-note-text');
    save.addEventListener('click', () => this._saveNote(text.value, expl, save));
    // Ctrl/Cmd+Enter from the box itself, so the thought can be finished
    // without reaching for a button that may be off-screen on a phone.
    text.addEventListener('keydown', e => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
        this._saveNote(text.value, expl, save);
      }
    });
  }

  /**
   * Record a note against the board, and the bid if one is selected.
   *
   * The page holds the whole board payload, so the note carries it: the
   * durable `file#board` reference, the hands, both auctions and the rules
   * behind our calls. A note that cannot say which board it is about stops
   * being actionable within the day.
   */
  async _saveNote(text, expl, button) {
    if (!text || !text.trim()) {
      toast('Write something first — the note is the whole point.', 'error');
      return;
    }
    const bid = expl ? {
      table:      this.selectedBid?.table,
      n:          this.selectedBid?.call_n,
      seat:       expl.seat,
      call:       expl.call,
      rule_id:    expl.rule_id,
      context_id: expl.context_id,
      shows:      expl.shows,
    } : null;

    const label = button?.textContent;
    if (button) { button.disabled = true; button.textContent = 'Saving…'; }
    try {
      const note = await apiFetch('/api/notes', {
        method: 'POST',
        body: JSON.stringify({ text, deal: this.currentDeal, bid }),
      });
      const where = note.deal ? ` on ${note.deal.ref}` : '';
      toast(`Saved ${note.id}${where}. It is in the Notes list for Claude.`,
            'success');
      const box = document.getElementById('dv-note-text');
      if (box) box.value = '';
      const general = document.getElementById('dv-note-text-general');
      if (general) general.value = '';
      this._refreshNoteCount();
    } catch (err) {
      toast(`Could not save the note: ${err.message}`, 'error');
    } finally {
      if (button) { button.disabled = false; button.textContent = label; }
    }
  }

  async _refreshNoteCount() {
    try {
      const data = await apiFetch('/api/notes');
      this.noteCount = (data.notes || []).filter(n => n.status !== 'done').length;
    } catch { this.noteCount = null; }
    this._renderActionFooter(this.currentDeal);
  }

  // -------------------------------------------------------------------------
  // Actions
  // -------------------------------------------------------------------------

  nextDeal() {
    this.currentDeal = null;
    this.selectedBid = null;
    this.lastExplanation = null;
    document.getElementById('dv-content').classList.add('hidden');
    this._hideInspector();
    document.getElementById('dv-btn-find').textContent = 'Find Deal';
    this.startGeneration();
  }

  /**
   * Keep the board for the lifetime of the tab.
   *
   * sessionStorage rather than localStorage: this is working state, and a
   * board resurrected days later in a new session would be confusing rather
   * than helpful. It survives what actually loses it — navigating away and
   * back, and a reload.
   */
  _saveDeal(deal) {
    try { sessionStorage.setItem('current_deal', JSON.stringify(deal)); }
    catch { /* private mode */ }
  }

  _loadDeal() {
    try {
      const raw = sessionStorage.getItem('current_deal');
      return raw ? JSON.parse(raw) : null;
    } catch { return null; }
  }

  _clearDeal() {
    try { sessionStorage.removeItem('current_deal'); } catch { /* as above */ }
  }

  _showError(msg) {
    const el = document.getElementById('dv-error');
    if (!el) return;
    el.textContent = msg;
    el.classList.remove('hidden');
    setTimeout(() => el.classList.add('hidden'), 6000);
  }
}
