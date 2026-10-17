(() => {
  const alerts = [
    {severity:'Critical',name:'Repeated authentication failures',detail:'Possible password spraying pattern',asset:'DEMO-AD-01',time:'14:21:08',confidence:92,status:'Investigating'},
    {severity:'High',name:'Suspicious outbound connection',detail:'Destination requires analyst validation',asset:'DEMO-WKS-14',time:'14:16:42',confidence:84,status:'Open'},
    {severity:'High',name:'Unusual PowerShell activity',detail:'Encoded command pattern matched',asset:'DEMO-ENDP-07',time:'14:02:19',confidence:81,status:'Needs review'},
    {severity:'Medium',name:'Multiple failed logins',detail:'Threshold exceeded in sample window',asset:'DEMO-APP-03',time:'13:58:51',confidence:68,status:'Open'},
    {severity:'Medium',name:'New service creation event',detail:'Validate against approved change window',asset:'DEMO-SRV-02',time:'13:41:05',confidence:63,status:'Needs review'}
  ];
  const $ = (id) => document.getElementById(id);
  const rows = $('alert-rows');
  const search = $('alert-search');
  const filter = $('severity-filter');
  const toast = $('toast');
  let toastTimer;
  const notify = (message) => {
    toast.textContent = message;
    toast.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.remove('show'), 3000);
  };
  function renderAlerts() {
    const query = (search?.value || '').trim().toLowerCase();
    const severity = filter?.value || 'all';
    const filtered = alerts.filter((a) => (severity === 'all' || a.severity === severity) && `${a.name} ${a.detail} ${a.asset} ${a.status}`.toLowerCase().includes(query));
    rows.innerHTML = '';
    filtered.forEach((a) => {
      const tr = document.createElement('tr');
      const sevClass = a.severity.toLowerCase();
      const statusClass = a.status === 'Investigating' ? 'investigating' : a.status === 'Open' ? 'open' : 'review';
      const cells = [
        `<span class="severity-label sev-${sevClass}">${a.severity}</span>`,
        `<span class="detection">${a.name}</span><span class="subtext">${a.detail}</span>`,
        `${a.asset}<span class="subtext">Sample asset</span>`,
        a.time,
        `<span class="confidence">${a.confidence}%</span>`,
        `<span class="status ${statusClass}">${a.status}</span>`
      ];
      cells.forEach((html) => { const td = document.createElement('td'); td.innerHTML = html; tr.appendChild(td); });
      rows.appendChild(tr);
    });
    $('result-count').textContent = `Showing ${filtered.length} of ${alerts.length} sample alerts`;
    if (!filtered.length) { const tr = document.createElement('tr'); const td = document.createElement('td'); td.colSpan = 6; td.textContent = 'No sample alerts match your filters.'; td.style.textAlign = 'center'; td.style.padding = '24px'; tr.appendChild(td); rows.appendChild(tr); }
  }
  function updateClock() { const now = new Date(); $('clock').textContent = now.toLocaleTimeString([], {hour12:false}); }
  updateClock(); window.setInterval(updateClock, 1000);
  renderAlerts();
  search?.addEventListener('input', renderAlerts);
  filter?.addEventListener('change', renderAlerts);
  $('refresh')?.addEventListener('click', () => { updateClock(); renderAlerts(); notify('Demo view refreshed. Live telemetry is not connected.'); });
  $('export-btn')?.addEventListener('click', () => {
    const report = {product:'IamZer01 Sentinel',mode:'DEMO',generated_at:new Date().toISOString(),live_telemetry_verified:false,notice:'All records in this snapshot are illustrative sample fixtures.',alerts};
    const blob = new Blob([JSON.stringify(report, null, 2)], {type:'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a'); a.href = url; a.download = 'sentinel-demo-snapshot.json'; a.click(); URL.revokeObjectURL(url);
    notify('Demo snapshot exported as JSON.');
  });
  $('menu-toggle')?.addEventListener('click', () => document.querySelector('.sidebar')?.classList.toggle('open'));
  document.querySelectorAll('.nav-link').forEach((link) => link.addEventListener('click', (event) => {
    const target = link.getAttribute('href');
    if (target && !['#overview','#alerts'].includes(target)) { event.preventDefault(); notify(`${link.textContent.trim()} is planned for a future module.`); }
    document.querySelectorAll('.nav-link').forEach((item) => item.classList.remove('active'));
    link.classList.add('active');
    document.querySelector('.sidebar')?.classList.remove('open');
  }));
  $('time-range')?.addEventListener('change', () => notify('This chart currently uses illustrative demo data.')); 
})();
