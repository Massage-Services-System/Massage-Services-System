'use strict';
(() => {
  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
  const paths = {
    calendar: '<rect x="3" y="5" width="18" height="16" rx="3"/><path d="M7 3v4m10-4v4M3 11h18m-13 4h1m6 0h1m-8 3h1"/>',
    shield: '<path d="M12 3 20 6v6c0 5-8 9-8 9s-8-4-8-9V6l8-3Z"/><path d="m8 12 3 3 5-6"/>',
    lotus: '<path d="M12 21c-5-3-7-7 0-17 7 10 5 14 0 17Zm0 0C5 21 2 15 2 10c5 0 9 3 10 11Zm0 0c7 0 10-6 10-11-5 0-9 3-10 11Z"/><path d="M7 15C4 12 5 6 5 6l5 4m7 5c3-3 2-9 2-9l-5 4"/>',
    body: '<circle cx="12" cy="4" r="2"/><path d="m8 9-4 5m12-5 4 5M8 8l4 1 4-1m-4 1v7m0 0-4 6m4-6 4 6"/>',
    spark: '<path d="m12 2 2.5 7.5L22 12l-7.5 2.5L12 22l-2.5-7.5L2 12l7.5-2.5L12 2Z"/>',
    stones: '<ellipse cx="12" cy="18" rx="10" ry="4"/><path d="M4 15c-2-5 2-7 8-7s10 2 8 7M7 9c-1-4 1-6 5-6s6 2 5 6"/>',
    hands: '<path d="M3 17V9c0-2 3-2 3 0v4l3-3c2-2 4 0 2 2l-3 4m13 1V9c0-2-3-2-3 0v4l-3-3c-2-2-4 0-2 2l3 4M3 17l5 4m13-4-5 4M9 4l1-2m5 2-1-2"/>',
    leaf: '<path d="M20 3C10 1 2 7 5 15c7 8 17 0 15-12Z"/><path d="m4 21 12-13M7 17l-1-6m5 2 6 1"/>',
    wave: '<path d="M2 8c4-6 6 6 10 0s6 6 10 0M2 14c4-6 6 6 10 0s6 6 10 0M2 20c4-6 6 6 10 0s6 6 10 0"/>',
    close: '<path d="m6 6 12 12M18 6 6 18"/>',
    chevron: '<path d="m6 9 6 6 6-6"/>',
    info: '<circle cx="12" cy="12" r="9"/><path d="M12 11v6m0-10h.01"/>',
    check: '<path d="m5 12 5 5L20 7"/>',
    plus: '<path d="M12 5v14M5 12h14"/>',
    telegram: '<path d="m3 11 18-7-4 17-6-6-3 3 1-6 8-5-10 7-4-3Z"/>',
  };
  const icon = (name) => `<span class="icon" aria-hidden="true"><svg viewBox="0 0 24 24">${paths[name] || paths.lotus}</svg></span>`;
  function icons(root = document) { $$('[data-icon]', root).forEach(el => { el.innerHTML = `<svg viewBox="0 0 24 24" aria-hidden="true">${paths[el.dataset.icon] || paths.lotus}</svg>`; }); }
  const esc = (value) => String(value ?? '').replace(/[&<>"']/g, x => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[x]));
  const state = { services: [], therapists: [], zones: [], zone: null, filter: 'all', token: '', user: null, config: null, visits: [], booking: null, catalogRequest: 0, availabilityRequest: 0, submitting: false, cancelledId: null };
  try { state.token = localStorage.getItem('massage.session') || ''; } catch { /* Storage may be disabled in the host. */ }
  const apiBase = (window.MASSAGE_API_BASE || '').replace(/\/$/, '') + '/api/v1';
  async function api(path, options = {}) {
    const headers = { 'Content-Type': 'application/json', ...options.headers };
    if (state.token) headers.Authorization = `Bearer ${state.token}`;
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 12000);
    try {
      const response = await fetch(apiBase + path, { ...options, headers, signal: controller.signal });
      const data = await response.json().catch(() => ({}));
      if (!response.ok) {
        if (response.status === 401) { state.user = null; saveToken(''); }
        const error = new Error(data.error?.message || 'Nie udało się wykonać operacji. Spróbuj ponownie.');
        error.code = data.error?.code; error.status = response.status; throw error;
      }
      return data;
    } catch (error) {
      if (error.name === 'AbortError') throw new Error('Serwer odpowiada zbyt długo. Spróbuj ponownie.');
      if (error instanceof TypeError) throw new Error('Brak połączenia z serwerem. Sprawdź internet i spróbuj ponownie.');
      throw error;
    } finally { clearTimeout(timeout); }
  }
  function saveToken(token) { state.token = token; try { token ? localStorage.setItem('massage.session', token) : localStorage.removeItem('massage.session'); } catch {} }
  let authPromise;
  async function ensureAuth() {
    if (state.user) return state.user;
    if (state.token) {
      try { state.user = await api('/me'); updateSession(); return state.user; }
      catch (error) { if (error.status !== 401) throw error; saveToken(''); }
    }
    if (!state.config?.demo_available) throw new Error('Na tym etapie działa lokalny podgląd; integracja Telegram dojdzie w zadaniu #9.');
    const result = await api('/auth/demo', {method:'POST', body:'{}'});
    saveToken(result.access_token); state.user = result.user; updateSession(); return state.user;
  }
  function updateSession() {
    const label = $('#session-label');
    if (state.user) { label.textContent = state.user.demo ? '✧ Podgląd lokalny' : `✧ Witaj, ${state.user.name}`; label.title = state.user.demo ? 'Rezerwacje testowe — oddzielne od kont Telegram' : ''; }
  }
  let toastTimer;
  function toast(message) { const el = $('#toast'); el.textContent = message; el.hidden = false; clearTimeout(toastTimer); toastTimer = setTimeout(() => { el.hidden = true; }, 4500); }
  function inlineError(id, error) { const el = $(id); el.textContent = error?.message || String(error); el.hidden = false; }
  function localDate(offset = 0) {
    const parts = new Intl.DateTimeFormat('en-CA', {timeZone:'Europe/Warsaw',year:'numeric',month:'2-digit',day:'2-digit'}).formatToParts(new Date());
    const get = type => parts.find(x => x.type === type).value;
    const date = new Date(`${get('year')}-${get('month')}-${get('day')}T12:00:00Z`);
    date.setUTCDate(date.getUTCDate() + offset); return date.toISOString().slice(0,10);
  }
  const formatDate = date => new Intl.DateTimeFormat('pl-PL', {day:'numeric', month:'long', year:'numeric', timeZone:'Europe/Warsaw'}).format(new Date(`${date}T12:00:00Z`));
  function showHome(scrollToCatalog = false) {
    $('#home-view').hidden = false; $('#visits-view').hidden = true;
    $$('[data-nav]').forEach(el => el.classList.toggle('active', el.dataset.nav === (scrollToCatalog ? 'massages' : 'home')));
    if (scrollToCatalog) $('#rituals').scrollIntoView({behavior:'smooth'}); else window.scrollTo({top:0, behavior:'smooth'});
  }
  function renderZoneList() {
    $('#zone-list').innerHTML = state.zones.map(zone => `<button data-zone-choice="${esc(zone.id)}" aria-pressed="${zone.id === state.zone}" class="${zone.id === state.zone ? 'active' : ''}">${esc(zone.name)}</button>`).join('');
  }
  async function selectZone(zone) {
    state.zone = state.zone === zone ? null : zone;
    state.filter = 'all';
    $$('[data-filter]').forEach(el => { const active = el.dataset.filter === 'all'; el.classList.toggle('active', active); el.setAttribute('aria-pressed', active); });
    $$('.body-zone').forEach(el => { const active = el.dataset.zone === state.zone; el.classList.toggle('selected', active); el.setAttribute('aria-pressed', active); });
    renderZoneList(); $('#reset-zone').hidden = !state.zone;
    const context = $('#zone-context'); context.hidden = !state.zone;
    if (state.zone) context.innerHTML = `Wybrana strefa: <strong>${esc(state.zones.find(z => z.id === state.zone)?.name || '')}</strong> <span>· Masaże dopasowane do Twojego wyboru</span>`;
    await loadCatalog();
  }
  function renderServices() {
    const services = state.services.filter(s => state.filter === 'all' || s.category === state.filter);
    $('#catalog-count').textContent = `${services.length} ${services.length === 1 ? 'masaż' : services.length < 5 ? 'masaże' : 'masaży'}`;
    $('#service-grid').innerHTML = services.length ? services.map(s => `<article class="service-card"><div class="service-top"><div class="service-icon">${icon(s.icon)}</div><span class="service-category">${esc(s.category)}</span></div><h3>${esc(s.name)}</h3><p>${esc(s.description)}</p><div class="service-bottom"><div class="service-meta"><span class="duration">${s.duration} min</span><span class="price">${s.price} <small>zł</small></span></div><button class="choose-service" data-service="${s.id}" aria-label="Wybierz ${esc(s.name)}">Wybierz</button></div></article>`).join('') : `<div class="empty-state">${icon('lotus')}<p>Brak masaży w tej kategorii dla wybranej strefy.</p><button class="text-link" data-reset-filters>Pokaż wszystkie masaże</button></div>`;
  }
  async function loadCatalog() {
    const requestId = ++state.catalogRequest;
    $('#catalog-error').hidden = true;
    $('#service-grid').innerHTML = '<div class="loading-state"><span class="spinner"></span>Przygotowujemy Twoją chwilę spokoju…</div>';
    try {
      const services = await api('/massages' + (state.zone ? `?zone=${encodeURIComponent(state.zone)}` : ''));
      if (requestId !== state.catalogRequest) return;
      state.services = services; renderServices();
    } catch (error) {
      if (requestId !== state.catalogRequest) return;
      $('#service-grid').innerHTML = '<div class="empty-state"><p>Oferta jest chwilowo niedostępna.</p><button class="btn btn-outline" data-retry-catalog>Spróbuj ponownie</button></div>';
      inlineError('#catalog-error', error);
    }
  }
  async function openBooking(serviceId) {
    toast('Proces rezerwacji zostanie dodany w zadaniu #7.');
  }
  function renderQuickDates() {
    return;
  }
  async function loadAvailability() {
    return;
  }
  function setBookingStage(stage) {
    return;
  }
  async function bookingNext() {
    return;
  }
  async function updateVisitCount() {
    return;
  }
  function renderVisits() {
    return;
  }
  async function showVisits() {
    toast('Sekcja Moje wizyty zostanie dodana w zadaniu #8.');
  }
  async function cancelVisit() {
    return;
  }
  document.addEventListener('click', async event => {
    const target = event.target.closest('button, a, [data-zone]');
    if (!target) return;
    if (target.matches('.brand')) { event.preventDefault(); showHome(); }
    else if (target.dataset.nav === 'visits') await showVisits();
    else if (target.dataset.nav === 'home') showHome();
    else if (target.dataset.nav === 'massages' || target.dataset.action === 'browse') showHome(true);
    else if (target.hasAttribute('data-zone-choice')) await selectZone(target.dataset.zoneChoice);
    else if (target.matches('[data-zone]')) await selectZone(target.dataset.zone);
    else if (target.id === 'reset-zone' || target.hasAttribute('data-reset-filters')) await selectZone(state.zone);
    else if (target.dataset.bodyView) {
      const back = target.dataset.bodyView === 'back';
      $$('[data-body-view]').forEach(el => { const active = el === target; el.classList.toggle('active', active); el.setAttribute('aria-pressed', active); });
      $('.back-zone').style.display = back ? '' : 'none'; $('.back-zone').setAttribute('tabindex', back ? '0' : '-1'); $('#body-side-label').textContent = back ? 'TYŁ CIAŁA' : 'PRZÓD CIAŁA';
    } else if (target.dataset.filter) {
      state.filter = target.dataset.filter;
      $$('[data-filter]').forEach(el => { const active = el === target; el.classList.toggle('active', active); el.setAttribute('aria-pressed', active); }); renderServices();
    } else if (target.dataset.service) await openBooking(target.dataset.service);
    else if (target.dataset.quickDate && state.booking) { state.booking.date = target.dataset.quickDate; $('#booking-date').value = state.booking.date; renderQuickDates(); await loadAvailability(); }
    else if (target.dataset.time && state.booking) {
      state.booking.time = target.dataset.time;
      $$('[data-time]').forEach(el => { const active = el === target; el.classList.toggle('active', active); el.setAttribute('aria-pressed', active); }); $('#booking-next').disabled = false;
    } else if (target.id === 'booking-next') await bookingNext();
    else if (target.id === 'booking-back') { $('#booking-error').hidden = true; setBookingStage(0); }
    else if (target.dataset.close && !state.submitting) $( '#' + target.dataset.close).close();
    else if (target.id === 'success-visits') { $('#booking-dialog').close(); await showVisits(); }
    else if (target.dataset.cancel) { state.cancelledId = target.dataset.cancel; $('#cancel-error').hidden = true; $('#cancel-dialog').showModal(); }
    else if (target.id === 'confirm-cancel') await cancelVisit();
    else if (target.hasAttribute('data-retry-catalog')) await loadCatalog();
    else if (target.hasAttribute('data-retry-slots')) await loadAvailability();
    else if (target.hasAttribute('data-retry-visits')) await showVisits();
  });
  $('#body-map').addEventListener('keydown', event => { const zone = event.target.closest('[data-zone]'); if (zone && (event.key === 'Enter' || event.key === ' ')) { event.preventDefault(); selectZone(zone.dataset.zone); } });
  $('#therapist-select').addEventListener('change', async event => { state.booking.therapist = Number(event.target.value); $('#therapist-specialty').textContent = state.therapists.find(t => t.id === state.booking.therapist)?.specialty || ''; await loadAvailability(); });
  $('#booking-date').addEventListener('change', async event => { state.booking.date = event.target.value; renderQuickDates(); await loadAvailability(); });
  $('#booking-dialog').addEventListener('close', () => { state.availabilityRequest++; });
  $$('dialog').forEach(dialog => { dialog.addEventListener('cancel', event => { if (state.submitting) event.preventDefault(); }); });
  $('#confirm-cancel').addEventListener('keydown', event => { if (event.key === 'Enter' && state.submitting) event.preventDefault(); });
  async function boot() {
    icons();
    try {
      const [config, zones, therapists] = await Promise.all([api('/config'), api('/zones'), api('/therapists')]);
      state.config = config; state.zones = zones; state.therapists = therapists; renderZoneList();
      await loadCatalog();
      if (state.token) { ensureAuth().then(updateVisitCount).catch(error => toast(error.message)); }
    } catch (error) {
      inlineError('#catalog-error', error); $('#service-grid').innerHTML = '<div class="empty-state"><p>Nie udało się połączyć z aplikacją.</p><button class="btn btn-outline" data-retry-boot>Odśwież połączenie</button></div>';
    }
  }
  document.addEventListener('click', event => { if (event.target.closest('[data-retry-boot]')) boot(); });
  boot();
})();
