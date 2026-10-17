(() => {
  const demoAlerts = [
    {severity:'Critical',name:'Repeated authentication failures',detail:'Possible password spraying pattern',asset:'DEMO-AD-01',time:'14:21:08',confidence:92,status:'Investigating'},
    {severity:'High',name:'Suspicious outbound connection',detail:'Destination requires analyst validation',asset:'DEMO-WKS-14',time:'14:16:42',confidence:84,status:'Open'},
    {severity:'High',name:'Unusual PowerShell activity',detail:'Encoded command pattern matched',asset:'DEMO-ENDP-07',time:'14:02:19',confidence:81,status:'Needs review'},
    {severity:'Medium',name:'Multiple failed logins',detail:'Threshold exceeded in sample window',asset:'DEMO-APP-03',time:'13:58:51',confidence:68,status:'Open'},
    {severity:'Medium',name:'New service creation event',detail:'Validate against approved change window',asset:'DEMO-SRV-02',time:'13:41:05',confidence:63,status:'Needs review'}
  ];
  const API_BASE = String(window.SENTINEL_CONFIG?.apiBase || '').trim().replace(/\/+$/, '');
  const $ = (id) => document.getElementById(id);
  const rows = $('alert-rows');
  const search = $('alert-search');
  const filter = $('severity-filter');
  const toast = $('toast');
  let toastTimer;
  let alertData = demoAlerts;
  let dataMode = 'DEMO';
  const notify = (message) => {
    toast.textContent = message;
    toast.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = window.setTimeout(() => toast.classList.remove('show'), 3000);
  };
  const text = (tag, className, value) => {
    const el = document.createElement(tag);
    if (className) el.className = className;
    el.textContent = value == null || value === '' ? 'Unknown' : String(value);
    return el;
  };
  function renderAlerts() {
    const query = (search?.value || '').trim().toLowerCase();
    const severity = filter?.value || 'all';
    const filtered = alertData.filter((a) => (severity === 'all' || a.severity.toLowerCase() === severity.toLowerCase()) && `${a.name} ${a.detail} ${a.asset} ${a.status}`.toLowerCase().includes(query));
    rows.replaceChildren();
    filtered.forEach((a) => {
      const tr = document.createElement('tr');
      const sev = text('span', `severity-label sev-${a.severity.toLowerCase()}`, a.severity);
      const title = text('span', 'detection', a.name);
      const detail = text('span', 'subtext', a.detail);
      const detection = document.createElement('td'); detection.append(title, detail);
      const asset = document.createElement('td'); asset.append(text('span', '', a.asset), text('span', 'subtext', a.source || (dataMode === 'DEMO' ? 'Sample asset' : 'API event')));
      const statusClass = /investigat/i.test(a.status) ? 'investigating' : /^open$/i.test(a.status) || /^new$/i.test(a.status) ? 'open' : 'review';
      const cells = [document.createElement('td'), detection, asset, text('td', '', a.time), document.createElement('td'), document.createElement('td')];
      cells[0].append(sev);
      cells[4].append(text('span', 'confidence', a.confidence == null ? 'Unknown' : `${a.confidence}%`));
      cells[5].append(text('span', `status ${statusClass}`, a.status));
      cells.forEach((td) => tr.appendChild(td));
      rows.appendChild(tr);
    });
    $('result-count').textContent = dataMode === 'DEMO'
      ? `Showing ${filtered.length} of ${alertData.length} sample alerts`
      : `Showing ${filtered.length} of ${alertData.length} API alerts`;
    if (!filtered.length) {
      const tr = document.createElement('tr');
      const td = text('td', '', 'No alerts match your filters.');
      td.colSpan = 6; td.style.textAlign = 'center'; td.style.padding = '24px';
      tr.appendChild(td); rows.appendChild(tr);
    }
  }
  function updateClock() {
    $('clock').textContent = new Date().toLocaleTimeString([], {hour12:false});
  }
  function setMode(mode, message) {
    dataMode = mode;
    const pill = document.querySelector('.demo-pill');
    if (pill) {
      pill.textContent = mode === 'DEMO' ? '● DEMO DATA' : '● API DATA';
      pill.classList.toggle('api-pill', mode === 'API');
    }
    const notice = document.querySelector('.notice');
    if (notice) {
      const heading = notice.querySelector('b');
      const paragraph = notice.querySelector('p');
      if (mode === 'API') {
        if (heading) heading.textContent = 'Backend API connected — alert queue uses API responses';
        if (paragraph) paragraph.textContent = 'The KPI cards and charts remain illustrative. A successful API response does not prove Wazuh or other upstream telemetry is connected.';
        notice.classList.add('api-notice');
        notice.querySelector('span')?.remove();
      } else {
        if (heading) heading.textContent = 'Preview environment — sample events only';
        if (paragraph) paragraph.textContent = 'Metrics below are illustrative fixtures. No live Wazuh, Prometheus, or Elasticsearch connection has been verified.';
        notice.classList.remove('api-notice');
        if (!notice.querySelector('span')) notice.append(text('span', '', 'NOT LIVE'));
      }
    }
    if (message) notify(message);
  }
  function normalizeAlert(item) {
    const severityRaw = String(item.severity || 'medium').toLowerCase();
    const severity = ['critical','high','medium','low'].includes(severityRaw) ? severityRaw[0].toUpperCase() + severityRaw.slice(1) : 'Medium';
    const stamp = item.timestamp || item.created_at || item.time;
    const parsed = stamp ? new Date(stamp) : null;
    return {
      severity,
      name: item.title || item.name || item.rule_name || 'Security alert',
      detail: item.description || item.message || item.rule_id || 'No description provided by API',
      asset: item.hostname || item.host || item.source_ip || 'Unknown asset',
      source: item.source || 'Backend API',
      time: parsed && !Number.isNaN(parsed.getTime()) ? parsed.toLocaleTimeString([], {hour12:false,timeZone:'UTC'}) : 'Unknown',
      confidence: item.confidence == null ? null : Math.max(0, Math.min(100, Number(item.confidence))),
      status: String(item.status || 'New').replaceAll('_',' ').replace(/\b\w/g, c => c.toUpperCase())
    };
  }
  async function loadApiAlerts() {
    if (!API_BASE) {
      alertData = demoAlerts;
      setMode('DEMO');
      renderAlerts();
      return false;
    }
    try {
      const response = await fetch(`${API_BASE}/api/v1/alerts?hours=24&limit=100`, {headers:{Accept:'application/json'}, credentials:'omit', mode:'cors', cache:'no-store'});
      if (!response.ok) throw new Error(`API returned HTTP ${response.status}`);
      const payload = await response.json();
      if (!Array.isArray(payload.alerts)) throw new Error('Unexpected alerts API response');
      alertData = payload.alerts.map(normalizeAlert);
      dataMode = 'API';
      setMode('API');
      renderAlerts();
      return true;
    } catch (_) {
      alertData = demoAlerts;
      setMode('DEMO');
      renderAlerts();
      return false;
    }
  }
  updateClock();
  window.setInterval(updateClock, 1000);
  renderAlerts();
  loadApiAlerts();
  search?.addEventListener('input', renderAlerts);
  filter?.addEventListener('change', renderAlerts);
  $('refresh')?.addEventListener('click', async () => {
    updateClock();
    const connected = await loadApiAlerts();
    notify(connected ? 'Alert queue refreshed from backend API.' : 'Showing demo alerts; backend API is unavailable at this site origin.');
  });
  $('export-btn')?.addEventListener('click', () => {
    const report = {product:'IamZer01 Sentinel',mode:dataMode,generated_at:new Date().toISOString(),live_upstream_telemetry_verified:false,notice:dataMode === 'DEMO' ? 'Illustrative sample fixtures.' : 'Alerts retrieved from the backend API; upstream source health is not asserted.',alerts:alertData};
    const blob = new Blob([JSON.stringify(report, null, 2)], {type:'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a'); a.href = url; a.download = 'sentinel-alert-snapshot.json'; a.click();
    window.setTimeout(() => URL.revokeObjectURL(url), 1000);
    notify('Alert snapshot exported as JSON.');
  });
  $('menu-toggle')?.addEventListener('click', () => document.querySelector('.sidebar')?.classList.toggle('open'));
  document.querySelectorAll('.nav-link').forEach((link) => link.addEventListener('click', (event) => {
    const target = link.getAttribute('href');
    if (target && !['#overview','#alerts'].includes(target)) {
      event.preventDefault();
      notify(`${link.textContent.trim()} is a planned module; its workflow is not implemented yet.`);
    }
    document.querySelectorAll('.nav-link').forEach((item) => item.classList.remove('active'));
    link.classList.add('active');
    document.querySelector('.sidebar')?.classList.remove('open');
  }));
  $('time-range')?.addEventListener('change', () => notify('The threat activity chart currently uses illustrative demo data.'));
})();