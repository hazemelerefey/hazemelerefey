const fs = require('fs');
const username = 'hazemelerefey';
const token = process.env.GITHUB_TOKEN;
async function fetchJSON(url) {
  const res = await fetch(url, {
    headers: {
      Accept: 'application/vnd.github+json',
      Authorization: `Bearer ${token}`,
      'User-Agent': 'hazemelerefey-dashboard'
    }
  });
  if (!res.ok) throw new Error(`HTTP ${res.status} for ${url}`);
  return res.json();
}
function formatNumber(n) {
  return n.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}
function escapeXml(str) {
  return str.replace(/[<>&'"]/g, c => {
    switch (c) {
      case '<': return '&lt;';
      case '>': return '&gt;';
      case '&': return '&amp;';
      case "'": return '&apos;';
      case '"': return '&quot;';
    }
  });
}
(async () => {
  try {
    const user = await fetchJSON(`https://api.github.com/users/${username}`);
    const repos = await fetchJSON(`https://api.github.com/users/${username}/repos?per_page=100&sort=pushed`);
    const stars = repos.reduce((sum, r) => sum + (r.stargazers_count || 0), 0);
    const forks = repos.reduce((sum, r) => sum + (r.forks_count || 0), 0);
    const latest = repos[0];
    const latestName = latest ? escapeXml(latest.name) : '\u2014';
    const latestDesc = latest && latest.description ? escapeXml(latest.description.slice(0, 55)) : 'No description';
    const latestUpdated = latest ? new Date(latest.pushed_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }) : '\u2014';
    const today = new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    const svg = `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="800" height="260" viewBox="0 0 800 260" role="img" aria-label="Live GitHub dashboard for Hazem Elerefy">
  <title>Live GitHub Dashboard</title>
  <desc>Shows public repositories, stars, followers, and latest activity for Hazem Elerefy.</desc>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0b0427"/>
      <stop offset="100%" stop-color="#1a103c"/>
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2.5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <style>
      .mono { font-family: 'JetBrains Mono', 'SFMono-Regular', 'Fira Code', monospace; }
      .label { fill: #94a3b8; font-size: 12px; }
      .value { fill: #e2e8f0; font-size: 22px; font-weight: 700; }
      .accent { fill: #22d3ee; }
      .purple { fill: #a78bfa; }
      .pink { fill: #f472b6; }
      .title { fill: #a78bfa; font-size: 20px; font-weight: 700; }
      .subtitle { fill: #22d3ee; font-size: 13px; }
      .box { fill: none; stroke: #334155; stroke-width: 1; }
      @media (prefers-color-scheme: light) {
        .value { fill: #0f172a; }
        .label { fill: #475569; }
        .title { fill: #7c3aed; }
        .subtitle { fill: #0891b2; }
        .box { stroke: #cbd5e1; }
      }
    </style>
  </defs>

  <rect width="800" height="260" rx="16" fill="url(#bg)"/>

  <text x="30" y="45" class="mono title" filter="url(#glow)">LIVE TELEMETRY</text>
  <text x="30" y="68" class="mono subtitle">${username} / github / ${today}</text>

  <line x1="30" y1="85" x2="770" y2="85" stroke="#334155" stroke-width="1"/>

  <g transform="translate(30, 110)">
    <rect width="170" height="80" rx="10" class="box"/>
    <text x="15" y="25" class="mono label">REPOSITORIES</text>
    <text x="15" y="58" class="mono value accent">${formatNumber(user.public_repos)}</text>
  </g>

  <g transform="translate(220, 110)">
    <rect width="170" height="80" rx="10" class="box"/>
    <text x="15" y="25" class="mono label">TOTAL STARS</text>
    <text x="15" y="58" class="mono value purple">${formatNumber(stars)}</text>
  </g>

  <g transform="translate(410, 110)">
    <rect width="170" height="80" rx="10" class="box"/>
    <text x="15" y="25" class="mono label">FOLLOWERS</text>
    <text x="15" y="58" class="mono value pink">${formatNumber(user.followers)}</text>
  </g>

  <g transform="translate(600, 110)">
    <rect width="170" height="80" rx="10" class="box"/>
    <text x="15" y="25" class="mono label">FORKS</text>
    <text x="15" y="58" class="mono value accent">${formatNumber(forks)}</text>
  </g>

  <g transform="translate(30, 210)">
    <text x="0" y="0" class="mono label">LATEST SHIP</text>
    <text x="0" y="22" class="mono value" font-size="15" fill="#e2e8f0">${latestName}</text>
    <text x="0" y="40" class="mono label" font-size="11">${latestDesc}</text>
    <text x="700" y="0" class="mono label" text-anchor="end">UPDATED</text>
    <text x="700" y="22" class="mono value" font-size="15" text-anchor="end" fill="#e2e8f0">${latestUpdated}</text>
  </g>
</svg>`;
    fs.writeFileSync('assets/dashboard-live.svg', svg.trim());
    console.log('\u2705 dashboard-live.svg generated');
  } catch (err) {
    console.error('\u274c Error generating dashboard:', err.message);
    process.exit(1);
  }
})();
