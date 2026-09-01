/**
 * ui.js — feedback and staged-patch state, shared by both views.
 *
 * Both pieces here exist because of the same failure: a user edited a rule,
 * pressed Save, saw nothing at all, and went looking for the change in
 * Proposals, where it also was not. The save had in fact failed — but the
 * message announcing that was rendered next to the editor's buttons, several
 * screens down on a phone, and removed itself after three and a half seconds.
 * Feedback nobody can see is the same as no feedback, and it is worse than
 * none when it is the only thing distinguishing "rejected" from "saved".
 */

// ---------------------------------------------------------------------------
// Toasts
// ---------------------------------------------------------------------------

function toastHost() {
  let host = document.getElementById('toast-host');
  if (!host) {
    host = document.createElement('div');
    host.id = 'toast-host';
    host.className = 'toast-host';
    document.body.appendChild(host);
  }
  return host;
}

/**
 * Show a message where the user is actually looking.
 *
 * Fixed to the viewport, so it does not matter how far the page has scrolled.
 * Success fades on its own; an error stays until dismissed, because an error
 * that times out is an error the user never read.
 */
export function toast(message, type = 'info') {
  const host = toastHost();
  const el = document.createElement('div');
  el.className = `toast toast-${type}`;
  el.setAttribute('role', type === 'error' ? 'alert' : 'status');

  const text = document.createElement('span');
  text.className = 'toast-text';
  text.textContent = message;
  el.appendChild(text);

  const close = document.createElement('button');
  close.className = 'toast-close';
  close.type = 'button';
  close.setAttribute('aria-label', 'Dismiss');
  close.textContent = '✕';
  close.addEventListener('click', () => el.remove());
  el.appendChild(close);

  host.appendChild(el);
  if (type !== 'error') setTimeout(() => el.remove(), 4500);
  return el;
}

// ---------------------------------------------------------------------------
// Staged patches
// ---------------------------------------------------------------------------

const KEY = 'staged_patches';

/**
 * Rule edits are STAGED, not submitted.
 *
 * Saving an edit puts a patch here; a proposal exists only once Submit
 * Proposal is pressed. That distinction is deliberate — several edits usually
 * belong in one proposal, and each proposal costs a corpus run — but it was
 * invisible, so a saved edit looked lost. Both views read this store now, so
 * the count can be shown wherever the user might go looking for it.
 */
export function loadStagedPatches() {
  try {
    const raw = JSON.parse(localStorage.getItem(KEY) || '[]');
    return Array.isArray(raw) ? raw : [];
  } catch {
    return [];
  }
}

export function saveStagedPatches(patches) {
  try {
    localStorage.setItem(KEY, JSON.stringify(patches));
  } catch { /* private mode, quota — the in-memory list still works */ }
}

export function clearStagedPatches() {
  try {
    localStorage.removeItem(KEY);
  } catch { /* as above */ }
}
