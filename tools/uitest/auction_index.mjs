/**
 * Does clicking a bid in the auction table explain THAT bid?
 *
 * Why this is a browser test.  The bug it guards against lived entirely in
 * the DOM: the table numbered our calls 0,1,2... as an ordinal among our own
 * calls, while the server keys decision setups by position in the full
 * auction.  Every Python test passed -- the server was right, the payload was
 * right -- and the page still explained the wrong bid, because nothing on
 * either side ever compared the number written into `data-call-n` against the
 * cell it was written on.  Only a real page with a real click closes that
 * loop.
 *
 * Two checks per engine-bid cell, over several deals:
 *   1. the cell's position in the rendered grid, offset by the dealer's
 *      column, equals its `data-call-n` -- so the seat a call is drawn under
 *      agrees with the index the click will send;
 *   2. clicking it opens an inspector showing the same call the cell shows.
 *
 * Usage:
 *   npm install playwright
 *   PYTHONPATH=src:tools python3 -m uvicorn bridgebidder.gui.app:app --port 8811
 *   node tools/uitest/auction_index.mjs
 *
 * BASE_URL, DEALS and PW_CHROMIUM (path to a Chromium build) override the
 * defaults.  Exits non-zero if any cell disagrees.
 */
import { chromium } from 'playwright';
const URL = process.env.BASE_URL || 'http://127.0.0.1:8811/';
const browser = await chromium.launch({ executablePath: process.env.PW_CHROMIUM || undefined });
const page = await browser.newPage({ viewport: { width: 1000, height: 1600 } });
const errs = [];
page.on('pageerror', e => errs.push('PAGEERROR ' + e.message));
page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
await page.goto(URL, { waitUntil: 'networkidle' });

const SEATS = ['W','N','E','S'];
let totalCells = 0, bad = 0, deals = 0;

const DEALS = Number(process.env.DEALS || 10);
for (let d = 0; d < DEALS; d++) {
  await page.click('#dv-btn-find');
  await page.waitForSelector('td.engine-bid', { timeout: 30000 });
  await page.waitForTimeout(300);
  deals++;

  // Read the rendered grid: every cell with its row/col, so we can check
  // seat placement independently of what the click handler believes.
  const grid = await page.$$eval('.auction-table-wrap', wraps => wraps.map(w => ({
    label: w.querySelector('.auction-table-label')?.textContent.trim(),
    rows: [...w.querySelectorAll('tbody tr')].map(tr =>
      [...tr.querySelectorAll('td')].map(td => ({
        text: td.textContent.trim(),
        empty: td.classList.contains('empty'),
        ours: td.classList.contains('engine-bid'),
        n: td.dataset.callN ? Number(td.dataset.callN) : null,
        id: td.id || null,
      }))),
  })));
  const dealer = (await page.textContent('.deal-meta-value')).trim();
  const dIdx = SEATS.indexOf(dealer);

  for (const [ti, tbl] of grid.entries()) {
    const tableKey = ti === 0 ? 'a' : 'b';
    // flatten grid positions -> auction index, and check seat column
    let pos = 0;
    for (const row of tbl.rows) {
      for (let col = 0; col < row.length; col++) {
        const cell = row[col];
        if (cell.empty || cell.text === '') { pos++; continue; }
        const auctionIdx = pos - dIdx;
        const seat = SEATS[pos % 4];
        if (cell.ours) {
          totalCells++;
          if (cell.n !== auctionIdx) {
            bad++;
            console.log(`  BAD INDEX ${tableKey} row-col ${pos}: cell "${cell.text}" seat ${seat} `
                      + `should be n=${auctionIdx} but data-call-n=${cell.n}`);
          } else {
            await page.click(`[id="${cell.id}"]`);
            await page.waitForFunction(() => {
              const el = document.querySelector('.inspector-rule-id');
              return el && el.textContent.trim() !== 'Loading…';
            }, { timeout: 15000 });
            const got = await page.evaluate(() => ({
              rule: document.querySelector('.inspector-rule-id')?.textContent.trim(),
              call: document.querySelector('.inspector-call')?.textContent.trim(),
            }));
            if (got.rule === 'Error' || got.call !== cell.text) {
              bad++;
              console.log(`  MISMATCH ${tableKey} n=${cell.n} seat ${seat} cell "${cell.text}" `
                        + `-> "${got.call}" / ${got.rule}`);
            }
          }
        }
        pos++;
      }
    }
  }
}
console.log(`\n${deals} deals · ${totalCells} engine cells checked · ${bad} bad`);
if (bad) process.exitCode = 1;
if (errs.length) { console.log('errors:'); [...new Set(errs)].slice(0,8).forEach(e => console.log('  ' + e)); }
await browser.close();
