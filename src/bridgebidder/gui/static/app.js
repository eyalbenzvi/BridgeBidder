/**
 * app.js — SPA router for Bridge Bidding Lab
 *
 * Hash-based routing: #deal (default) and #notes.
 * Each view is a class with render() and optional destroy().
 */

import { DealView }      from './deal-view.js';
import { NotesView }    from './notes-view.js';

const root = document.getElementById('app-root');
let currentView = null;

const navDeal      = document.getElementById('nav-deal');
const navNotes     = document.getElementById('nav-notes');

/**
 * Navigate to the view corresponding to the given hash.
 * Tears down the previous view and mounts a fresh one.
 */
function navigate(hash) {
  // Destroy previous view (WebSocket cleanup etc.)
  if (currentView && typeof currentView.destroy === 'function') {
    currentView.destroy();
  }
  root.innerHTML = '';

  const isNotes = hash === '#notes';

  navDeal.classList.toggle('active', !isNotes);
  navNotes.classList.toggle('active', isNotes);

  currentView = isNotes ? new NotesView(root) : new DealView(root);
  currentView.render();
}

window.addEventListener('hashchange', () => navigate(window.location.hash));

/**
 * Show which build is serving the page.
 *
 * A host that has not redeployed and a browser holding a cached module look
 * identical to a bug that was never fixed. This makes the difference visible
 * without anyone having to reason about it.
 */
async function showBuild() {
  const tag = document.getElementById('build-tag');
  if (!tag) return;
  try {
    const res = await fetch('/api/env', { cache: 'no-store' });
    const env = await res.json();
    tag.textContent = env.build || '';
    tag.title = `build ${env.build} · deals from ${env.deal_source}`;
  } catch {
    tag.textContent = '';
  }
}

// Boot
showBuild();
navigate(window.location.hash || '#deal');
