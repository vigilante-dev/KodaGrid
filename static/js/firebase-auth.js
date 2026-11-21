import { initializeApp } from 'https://www.gstatic.com/firebasejs/13.4.0/firebase-app.js';
import {
  getAuth,
  createUserWithEmailAndPassword,
  sendEmailVerification,
  signInWithEmailAndPassword,
} from 'https://www.gstatic.com/firebasejs/13.4.0/firebase-auth.js';

const panel = document.querySelector('.firebase-auth');
if (panel) {
  const app = initializeApp({
    apiKey: panel.dataset.apiKey,
    authDomain: panel.dataset.authDomain,
    projectId: panel.dataset.projectId,
    appId: panel.dataset.appId,
  });
  const auth = getAuth(app);
  const [emailField, passwordField] = panel.querySelectorAll('input');
  const button = panel.querySelector('[data-firebase-submit]');
  const status = panel.querySelector('[data-firebase-status]');

  button.addEventListener('click', async () => {
    button.disabled = true;
    status.textContent = 'Connecting securely...';
    try {
      let credential;
      if (panel.dataset.mode === 'register') {
        credential = await createUserWithEmailAndPassword(auth, emailField.value.trim(), passwordField.value);
        await sendEmailVerification(credential.user);
        status.textContent = 'Check your email and verify your address, then sign in.';
        await auth.signOut();
        return;
      }
      credential = await signInWithEmailAndPassword(auth, emailField.value.trim(), passwordField.value);
      if (!credential.user.emailVerified) {
        await sendEmailVerification(credential.user);
        status.textContent = 'Verify your email using the link we just sent, then sign in again.';
        return;
      }
      const idToken = await credential.user.getIdToken(true);
      const response = await fetch(panel.dataset.sessionUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'same-origin',
        body: JSON.stringify({ id_token: idToken }),
      });
      const result = await response.json();
      if (!response.ok) throw new Error(result.error || 'Sign-in failed.');
      window.location.assign(result.redirect);
    } catch (error) {
      status.textContent = error.message || 'Sign-in failed. Please try again.';
    } finally {
      button.disabled = false;
    }
  });
}
