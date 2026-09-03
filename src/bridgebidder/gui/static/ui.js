/**
 * ui.js — the toast, shared by both views.
 *
 * It exists because of a specific failure: a user saved a rule edit, saw
 * nothing at all, and went looking for the change on the other screen, where
 * it also was not. The save had in fact failed — but the message saying so
 * was rendered next to the editor's buttons, several screens down on a phone,
 * and removed itself after three and a half seconds. Feedback nobody can see
 * is the same as no feedback, and worse than none when it is the only thing
 * distinguishing "rejected" from "saved".
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
