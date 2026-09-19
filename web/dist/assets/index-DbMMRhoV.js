(function(){const a=document.createElement("link").relList;if(a&&a.supports&&a.supports("modulepreload"))return;for(const t of document.querySelectorAll('link[rel="modulepreload"]'))p(t);new MutationObserver(t=>{for(const n of t)if(n.type==="childList")for(const l of n.addedNodes)l.tagName==="LINK"&&l.rel==="modulepreload"&&p(l)}).observe(document,{childList:!0,subtree:!0});function h(t){const n={};return t.integrity&&(n.integrity=t.integrity),t.referrerPolicy&&(n.referrerPolicy=t.referrerPolicy),t.crossOrigin==="use-credentials"?n.credentials="include":t.crossOrigin==="anonymous"?n.credentials="omit":n.credentials="same-origin",n}function p(t){if(t.ep)return;t.ep=!0;const n=h(t);fetch(t.href,n)}})();const A="/api";async function i(e){const a=await fetch(`${A}${e}`);if(!a.ok)throw new Error(`API request failed: ${a.status} ${a.statusText}`);return a.json()}const r={health:()=>i("/health"),schools:()=>i("/schools"),school:e=>i(`/schools/${e}`),zones:()=>i("/zones"),zone:e=>i(`/zones/${e}`),events:()=>i("/events"),statistics:()=>i("/statistics"),heatmap:()=>i("/heatmap"),leaderboard:()=>i("/leaderboard"),achievements:()=>i("/achievements"),cameras:()=>i("/cameras"),camera:e=>i(`/cameras/${e}`),sensorReadings:()=>i("/sensors/readings"),awarenessQuestions:()=>i("/awareness/questions")};function D(){return`
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
  `}const d=document.querySelector("#app");function f(e){return`
    <nav class="top-nav">
      <a href="#dashboard" class="nav-link ${e==="dashboard"?"active":""}">Dashboard</a>
      <a href="#privacy" class="nav-link ${e==="privacy"?"active":""}">Privacy</a>
    </nav>
  `}async function M(){if(d)try{const[e,a,h,p,t,n,l,b]=await Promise.all([r.health(),r.statistics(),r.schools(),r.events(),r.heatmap(),r.achievements(),r.sensorReadings(),r.awarenessQuestions()]),c=h.schools??[],u=p.events??[],v=t.zones??[],g=n.achievements??[],$=l.readings??[],S=b.questions??[],m=c[0],w=c.reduce((s,o)=>s+(o.camera_count??0),0),_=c.reduce((s,o)=>s+(o.zone_count??0),0),k=c.reduce((s,o)=>s+(o.score??0),0);d.innerHTML=`
      ${f("dashboard")}
      <div class="dashboard">
        <header class="header">
          <div>
            <h1>AIRIS</h1>
            <div class="subtitle">Smoke-Free Campus</div>
          </div>
          <div class="badge">${e.demo_mode?"DEMO MODE":"LIVE MODE"} · ${e.sensor_zones??0} sensor zones</div>
        </header>

        <section class="system-status">
          <article class="card">
            <h3>Cameras Online</h3>
            <p class="metric">${w}</p>
          </article>
          <article class="card">
            <h3>Active Zones</h3>
            <p class="metric">${_}</p>
          </article>
          <article class="card">
            <h3>Events Today</h3>
            <p class="metric">${a.total_events}</p>
          </article>
          <article class="card">
            <h3>Smoke-Free Zones</h3>
            <p class="metric">${a.smoke_free_zones}</p>
          </article>
        </section>

        <section class="grid">
          <article class="card map-panel">
            <h3>Campus Map</h3>
            <div class="map-box">
              ${v.map((s,o)=>`
                    <div class="zone zone-${s.level}" style="left: ${10+o*20}%; top: ${15+o%2*25}%;">
                      ${s.zone_id}
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
              ${u.slice(0,4).map(s=>`
                    <li>
                      <span>${s.zone_id??"Zone"}</span>
                      <span>${s.event_type??"Smoke detected"}</span>
                      <span>${s.timestamp?new Date(s.timestamp).toLocaleTimeString([],{hour:"2-digit",minute:"2-digit"}):"--:--"}</span>
                    </li>
                  `).join("")}
            </ul>
          </article>
        </section>

        <section class="grid" style="margin-top: 20px;">
          <article class="card">
            <h3>School Score</h3>
            <ul class="score-list">
              ${c.map(s=>`<li><span>${s.school_name}</span><strong>${s.score} points</strong></li>`).join("")}
            </ul>
          </article>

          <article class="card">
            <h3>Achievements</h3>
            <ul class="achievement-list">
              ${g.slice(0,4).map(s=>`<li><strong>${s.badge} ${s.title}</strong></li>`).join("")}
            </ul>
          </article>
        </section>

        <section class="grid" style="margin-top: 20px;">
          <article class="card">
            <h3>Air Quality Sensors</h3>
            <ul class="list-table">
              ${$.length?$.map(s=>`<li><span>${s.zone_id}</span><strong>${s.smoke_alarm?"SMOKE ALARM":`PM2.5 ${s.pm25??"--"}`}</strong></li>`).join(""):"<li><span>No readings</span><em>Waiting for sensor data</em></li>"}
            </ul>
          </article>
          <article class="card">
            <h3>Daily Awareness</h3>
            <ul class="list-table">
              ${S.map(s=>`<li><span>${s.question}</span><strong>+${s.points}</strong></li>`).join("")}
            </ul>
          </article>
        </section>

        <section class="page-grid" style="margin-top: 20px;">
          <div class="stack">
            <div class="sheet">
              <h2>Camera Monitor</h2>
              <div class="toolbar">
                <select>
                  <option>${(m==null?void 0:m.school_name)??"School A"} Camera 1</option>
                </select>
                <button>Start Camera</button>
                <button class="secondary">Stop Camera</button>
              </div>
              <div class="camera-stage">Live camera preview</div>
              <div class="status-grid">
                <div class="mini-card"><span>AI status</span><strong>READY</strong></div>
                <div class="mini-card"><span>Detection</span><strong>SMOKE</strong></div>
                <div class="mini-card"><span>Confidence</span><strong>${(a.smoke_events/Math.max(a.total_events,1)).toFixed(2)}</strong></div>
              </div>
            </div>

            <div class="sheet">
              <h2>Recent Events</h2>
              <ul class="list-table">
                ${u.slice(0,3).map(s=>`<li><span>${s.zone_id??"Zone"}</span><em>${s.event_type??"Smoke"}</em><strong>${s.timestamp?new Date(s.timestamp).toLocaleTimeString([],{hour:"2-digit",minute:"2-digit"}):"--:--"}</strong></li>`).join("")}
              </ul>
            </div>
          </div>

          <div class="stack">
            <div class="sheet">
              <h2>Campus Map</h2>
              <div class="map-board">
                ${v.map((s,o)=>`<div class="zone-chip ${s.level}" style="left: ${10+o*18}%; top: ${20+o%2*28}%;">${s.zone_id}</div>`).join("")}
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
                ${v.slice(0,3).map(s=>`<div class="heat-cell ${s.level}">${s.level.toUpperCase()}</div>`).join("")}
              </div>
            </div>
          </div>

          <div class="stack">
            <div class="sheet">
              <h2>Statistics</h2>
              <div class="stats-grid">
                <div class="mini-card"><span>Total</span><strong>${a.total_events}</strong></div>
                <div class="mini-card"><span>Smoke</span><strong>${a.smoke_events}</strong></div>
                <div class="mini-card"><span>Active</span><strong>${a.active_cameras}</strong></div>
                <div class="mini-card"><span>Zones</span><strong>${a.monitored_zones}</strong></div>
                <div class="mini-card"><span>Free</span><strong>${a.smoke_free_zones}</strong></div>
                <div class="mini-card"><span>Score</span><strong>${k}</strong></div>
              </div>
              <div class="chart-box">
                ${(a.hourly??[]).slice(0,6).map(s=>`<div class="bar" style="height: ${Number(s.events??0)/5*100}%"></div>`).join("")}
              </div>
            </div>

            <div class="sheet">
              <h2>School System</h2>
              <ul class="list-table">
                ${c.map(s=>`<li><span>${s.school_name}</span><strong>${s.score} points</strong><em>+${s.improvement}%</em></li>`).join("")}
              </ul>
            </div>
          </div>

          <div class="stack">
            <div class="sheet">
              <h2>Achievements</h2>
              <ul class="list-table">
                ${g.slice(0,4).map(s=>`<li><span>${s.badge} ${s.title}</span><em>${s.school_id}</em></li>`).join("")}
              </ul>
            </div>
          </div>
        </section>
      </div>
    `}catch(e){d.innerHTML=`
      <div class="card" style="max-width: 700px; margin: 40px auto;">
        <h3>Dashboard unavailable</h3>
        <p>Unable to load AIRIS API data. Confirm the FastAPI backend is running on port 8000.</p>
        <pre>${e instanceof Error?e.message:String(e)}</pre>
      </div>
    `}}function z(){d&&(d.innerHTML=`${f("privacy")}${D()}`)}function y(){if(window.location.hash.replace("#","")==="privacy"){z();return}M()}window.addEventListener("hashchange",y);y();
