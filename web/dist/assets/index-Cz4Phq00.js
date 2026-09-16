(function(){const s=document.createElement("link").relList;if(s&&s.supports&&s.supports("modulepreload"))return;for(const t of document.querySelectorAll('link[rel="modulepreload"]'))d(t);new MutationObserver(t=>{for(const i of t)if(i.type==="childList")for(const c of i.addedNodes)c.tagName==="LINK"&&c.rel==="modulepreload"&&d(c)}).observe(document,{childList:!0,subtree:!0});function p(t){const i={};return t.integrity&&(i.integrity=t.integrity),t.referrerPolicy&&(i.referrerPolicy=t.referrerPolicy),t.crossOrigin==="use-credentials"?i.credentials="include":t.crossOrigin==="anonymous"?i.credentials="omit":i.credentials="same-origin",i}function d(t){if(t.ep)return;t.ep=!0;const i=p(t);fetch(t.href,i)}})();const S="/api";async function n(a){const s=await fetch(`${S}${a}`);if(!s.ok)throw new Error(`API request failed: ${s.status} ${s.statusText}`);return s.json()}const r={health:()=>n("/health"),schools:()=>n("/schools"),school:a=>n(`/schools/${a}`),zones:()=>n("/zones"),zone:a=>n(`/zones/${a}`),events:()=>n("/events"),statistics:()=>n("/statistics"),heatmap:()=>n("/heatmap"),leaderboard:()=>n("/leaderboard"),achievements:()=>n("/achievements"),cameras:()=>n("/cameras"),camera:a=>n(`/cameras/${a}`)};function _(){return`
    <div class="privacy-page">
      <h2>Privacy</h2>
      <div class="privacy-grid">
        <div class="sheet">
          <h3>What AIRIS collects</h3>
          <ul>
            <li>Aggregated smoke detection events</li>
            <li>Zone and camera metadata</li>
            <li>Time and confidence ranges</li>
            <li>Monitoring coverage and school-level status</li>
          </ul>
        </div>
        <div class="sheet">
          <h3>What AIRIS does not collect</h3>
          <ul>
            <li>Student names</li>
            <li>Student ID</li>
            <li>Face images or embeddings</li>
            <li>Behavioral profile of a person</li>
            <li>Track-to-person linkage</li>
          </ul>
        </div>
      </div>

      <div class="sheet">
        <h3>How processing works</h3>
        <p>
          Camera frames are processed in-memory for smoke detection. Raw frames are not retained as a public asset.
          Only minimal event metadata is recorded for safety monitoring and aggregated reporting.
        </p>
      </div>

      <div class="sheet">
        <h3>Storage and retention</h3>
        <p>
          Event metadata is stored for operational reporting and is kept to the minimum necessary for school-level monitoring.
          Retention periods are configurable and snapshots are not exposed through the public dashboard.
        </p>
      </div>
    </div>
  `}const l=document.querySelector("#app");function g(a){return`
    <nav class="top-nav">
      <a href="#dashboard" class="nav-link ${a==="dashboard"?"active":""}">Dashboard</a>
      <a href="#privacy" class="nav-link ${a==="privacy"?"active":""}">Privacy</a>
    </nav>
  `}async function w(){if(l)try{const[a,s,p,d,t,i]=await Promise.all([r.health(),r.statistics(),r.schools(),r.events(),r.heatmap(),r.achievements()]),c=p.schools??[],m=d.events??[],v=t.zones??[],u=i.achievements??[],h=c[0],f=c.reduce((e,o)=>e+(o.camera_count??0),0),y=c.reduce((e,o)=>e+(o.zone_count??0),0),b=c.reduce((e,o)=>e+(o.score??0),0);l.innerHTML=`
      ${g("dashboard")}
      <div class="dashboard">
        <header class="header">
          <div>
            <h1>AIRIS</h1>
            <div class="subtitle">Smoke-Free Campus</div>
          </div>
          <div class="badge">${a.demo_mode?"DEMO MODE":"LIVE MODE"}</div>
        </header>

        <section class="system-status">
          <article class="card">
            <h3>Cameras Online</h3>
            <p class="metric">${f}</p>
          </article>
          <article class="card">
            <h3>Active Zones</h3>
            <p class="metric">${y}</p>
          </article>
          <article class="card">
            <h3>Events Today</h3>
            <p class="metric">${s.total_events}</p>
          </article>
          <article class="card">
            <h3>Smoke-Free Zones</h3>
            <p class="metric">${s.smoke_free_zones}</p>
          </article>
        </section>

        <section class="grid">
          <article class="card map-panel">
            <h3>Campus Map</h3>
            <div class="map-box">
              ${v.map((e,o)=>`
                    <div class="zone zone-${e.level}" style="left: ${10+o*20}%; top: ${15+o%2*25}%;">
                      ${e.zone_id}
                    </div>
                  `).join("")}
            </div>
            <div class="heatmap-legend">
              <span class="legend-item"><span class="legend-swatch" style="background: var(--green);"></span>Low</span>
              <span class="legend-item"><span class="legend-swatch" style="background: var(--yellow);"></span>Medium</span>
              <span class="legend-item"><span class="legend-swatch" style="background: var(--red);"></span>High</span>
            </div>
          </article>

          <article class="card">
            <h3>Recent Events</h3>
            <ul class="event-list">
              ${m.slice(0,4).map(e=>`
                    <li>
                      <span>${e.zone_id??"Zone"}</span>
                      <span>${e.event_type??"Smoke detected"}</span>
                      <span>${e.timestamp?new Date(e.timestamp).toLocaleTimeString([],{hour:"2-digit",minute:"2-digit"}):"--:--"}</span>
                    </li>
                  `).join("")}
            </ul>
          </article>
        </section>

        <section class="grid" style="margin-top: 20px;">
          <article class="card">
            <h3>School Score</h3>
            <ul class="score-list">
              ${c.map(e=>`<li><span>${e.school_name}</span><strong>${e.score} points</strong></li>`).join("")}
            </ul>
          </article>

          <article class="card">
            <h3>Achievements</h3>
            <ul class="achievement-list">
              ${u.slice(0,4).map(e=>`<li><strong>${e.badge} ${e.title}</strong></li>`).join("")}
            </ul>
          </article>
        </section>

        <section class="page-grid" style="margin-top: 20px;">
          <div class="stack">
            <div class="sheet">
              <h2>Camera Monitor</h2>
              <div class="toolbar">
                <select>
                  <option>${(h==null?void 0:h.school_name)??"School A"} Camera 1</option>
                </select>
                <button>Start Camera</button>
                <button class="secondary">Stop Camera</button>
              </div>
              <div class="camera-stage">Live camera preview</div>
              <div class="status-grid">
                <div class="mini-card"><span>AI status</span><strong>READY</strong></div>
                <div class="mini-card"><span>Detection</span><strong>SMOKE</strong></div>
                <div class="mini-card"><span>Confidence</span><strong>${(s.smoke_events/Math.max(s.total_events,1)).toFixed(2)}</strong></div>
              </div>
            </div>

            <div class="sheet">
              <h2>Recent Events</h2>
              <ul class="list-table">
                ${m.slice(0,3).map(e=>`<li><span>${e.zone_id??"Zone"}</span><em>${e.event_type??"Smoke"}</em><strong>${e.timestamp?new Date(e.timestamp).toLocaleTimeString([],{hour:"2-digit",minute:"2-digit"}):"--:--"}</strong></li>`).join("")}
              </ul>
            </div>
          </div>

          <div class="stack">
            <div class="sheet">
              <h2>Campus Map</h2>
              <div class="map-board">
                ${v.map((e,o)=>`<div class="zone-chip ${e.level}" style="left: ${10+o*18}%; top: ${20+o%2*28}%;">${e.zone_id}</div>`).join("")}
              </div>
              <div class="legend-row">
                <span><i class="dot low"></i>Low</span>
                <span><i class="dot medium"></i>Medium</span>
                <span><i class="dot high"></i>High</span>
              </div>
            </div>

            <div class="sheet">
              <h2>Smoke Heatmap</h2>
              <div class="heat-grid">
                ${v.slice(0,3).map(e=>`<div class="heat-cell ${e.level}">${e.level.toUpperCase()}</div>`).join("")}
              </div>
            </div>
          </div>

          <div class="stack">
            <div class="sheet">
              <h2>Statistics</h2>
              <div class="stats-grid">
                <div class="mini-card"><span>Total</span><strong>${s.total_events}</strong></div>
                <div class="mini-card"><span>Smoke</span><strong>${s.smoke_events}</strong></div>
                <div class="mini-card"><span>Active</span><strong>${s.active_cameras}</strong></div>
                <div class="mini-card"><span>Zones</span><strong>${s.monitored_zones}</strong></div>
                <div class="mini-card"><span>Free</span><strong>${s.smoke_free_zones}</strong></div>
                <div class="mini-card"><span>Score</span><strong>${b}</strong></div>
              </div>
              <div class="chart-box">
                ${(s.hourly??[]).slice(0,6).map(e=>`<div class="bar" style="height: ${Number(e.events??0)/5*100}%"></div>`).join("")}
              </div>
            </div>

            <div class="sheet">
              <h2>School System</h2>
              <ul class="list-table">
                ${c.map(e=>`<li><span>${e.school_name}</span><strong>${e.score} points</strong><em>+${e.improvement}%</em></li>`).join("")}
              </ul>
            </div>
          </div>

          <div class="stack">
            <div class="sheet">
              <h2>Achievements</h2>
              <ul class="list-table">
                ${u.slice(0,4).map(e=>`<li><span>${e.badge} ${e.title}</span><em>${e.school_id}</em></li>`).join("")}
              </ul>
            </div>
          </div>
        </section>
      </div>
    `}catch(a){l.innerHTML=`
      <div class="card" style="max-width: 700px; margin: 40px auto;">
        <h3>Dashboard unavailable</h3>
        <p>Unable to load AIRIS API data. Confirm the FastAPI backend is running on port 8000.</p>
        <pre>${a instanceof Error?a.message:String(a)}</pre>
      </div>
    `}}function k(){l&&(l.innerHTML=`${g("privacy")}${_()}`)}function $(){if(window.location.hash.replace("#","")==="privacy"){k();return}w()}window.addEventListener("hashchange",$);$();
