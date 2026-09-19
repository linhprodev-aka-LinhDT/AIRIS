import './styles/main.css';
import { api } from './services/api';
import { PrivacyView } from './components/Privacy';

const app = document.querySelector('#app');

function renderNavigation(currentView: 'dashboard' | 'privacy') {
  return `
    <nav class="top-nav">
      <a href="#dashboard" class="nav-link ${currentView === 'dashboard' ? 'active' : ''}">Dashboard</a>
      <a href="#privacy" class="nav-link ${currentView === 'privacy' ? 'active' : ''}">Privacy</a>
    </nav>
  `;
}

async function loadDashboard() {
  if (!app) return;

  try {
    const [health, stats, schools, events, heatmap, achievements, sensors, awareness] = await Promise.all([
      api.health(),
      api.statistics(),
      api.schools(),
      api.events(),
      api.heatmap(),
      api.achievements(),
      api.sensorReadings(),
      api.awarenessQuestions(),
    ]);

    const schoolData = schools.schools ?? [];
    const eventData = events.events ?? [];
    const heatmapData = heatmap.zones ?? [];
    const achievementData = achievements.achievements ?? [];
    const sensorData = sensors.readings ?? [];
    const questionData = awareness.questions ?? [];

    const primarySchool = schoolData[0];
    const cameraCount = schoolData.reduce((sum, school) => sum + (school.camera_count ?? 0), 0);
    const activeZones = schoolData.reduce((sum, school) => sum + (school.zone_count ?? 0), 0);
    const totalSchoolScore = schoolData.reduce((sum, school) => sum + (school.score ?? 0), 0);

    app.innerHTML = `
      ${renderNavigation('dashboard')}
      <div class="dashboard">
        <header class="header">
          <div>
            <h1>AIRIS</h1>
            <div class="subtitle">Smoke-Free Campus</div>
          </div>
          <div class="badge">${health.demo_mode ? 'DEMO MODE' : 'LIVE MODE'} · ${health.sensor_zones ?? 0} sensor zones</div>
        </header>

        <section class="system-status">
          <article class="card">
            <h3>Cameras Online</h3>
            <p class="metric">${cameraCount}</p>
          </article>
          <article class="card">
            <h3>Active Zones</h3>
            <p class="metric">${activeZones}</p>
          </article>
          <article class="card">
            <h3>Events Today</h3>
            <p class="metric">${stats.total_events}</p>
          </article>
          <article class="card">
            <h3>Smoke-Free Zones</h3>
            <p class="metric">${stats.smoke_free_zones}</p>
          </article>
        </section>

        <section class="grid">
          <article class="card map-panel">
            <h3>Campus Map</h3>
            <div class="map-box">
              ${heatmapData
                .map(
                  (zone, index) => `
                    <div class="zone zone-${zone.level}" style="left: ${10 + (index * 20)}%; top: ${15 + (index % 2) * 25}%;">
                      ${zone.zone_id}
                    </div>
                  `,
                )
                .join('')}
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
              ${eventData
                .slice(0, 4)
                .map(
                  (event) => `
                    <li>
                      <span>${event.zone_id ?? 'Zone'}</span>
                      <span>${event.event_type ?? 'Smoke detected'}</span>
                      <span>${event.timestamp ? new Date(event.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : '--:--'}</span>
                    </li>
                  `,
                )
                .join('')}
            </ul>
          </article>
        </section>

        <section class="grid" style="margin-top: 20px;">
          <article class="card">
            <h3>School Score</h3>
            <ul class="score-list">
              ${schoolData
                .map(
                  (school) => `<li><span>${school.school_name}</span><strong>${school.score} points</strong></li>`,
                )
                .join('')}
            </ul>
          </article>

          <article class="card">
            <h3>Achievements</h3>
            <ul class="achievement-list">
              ${achievementData
                .slice(0, 4)
                .map(
                  (item) => `<li><strong>${item.badge} ${item.title}</strong></li>`,
                )
                .join('')}
            </ul>
          </article>
        </section>

        <section class="grid" style="margin-top: 20px;">
          <article class="card">
            <h3>Air Quality Sensors</h3>
            <ul class="list-table">
              ${sensorData.length ? sensorData.map((reading) => `<li><span>${reading.zone_id}</span><strong>${reading.smoke_alarm ? 'SMOKE ALARM' : `PM2.5 ${reading.pm25 ?? '--'}`}</strong></li>`).join('') : '<li><span>No readings</span><em>Waiting for sensor data</em></li>'}
            </ul>
          </article>
          <article class="card">
            <h3>Daily Awareness</h3>
            <ul class="list-table">
              ${questionData.map((item) => `<li><span>${item.question}</span><strong>+${item.points}</strong></li>`).join('')}
            </ul>
          </article>
        </section>

        <section class="page-grid" style="margin-top: 20px;">
          <div class="stack">
            <div class="sheet">
              <h2>Camera Monitor</h2>
              <div class="toolbar">
                <select>
                  <option>${primarySchool?.school_name ?? 'School A'} Camera 1</option>
                </select>
                <button>Start Camera</button>
                <button class="secondary">Stop Camera</button>
              </div>
              <div class="camera-stage">Live camera preview</div>
              <div class="status-grid">
                <div class="mini-card"><span>AI status</span><strong>READY</strong></div>
                <div class="mini-card"><span>Detection</span><strong>SMOKE</strong></div>
                <div class="mini-card"><span>Confidence</span><strong>${(stats.smoke_events / Math.max(stats.total_events, 1)).toFixed(2)}</strong></div>
              </div>
            </div>

            <div class="sheet">
              <h2>Recent Events</h2>
              <ul class="list-table">
                ${eventData
                  .slice(0, 3)
                  .map(
                    (event) => `<li><span>${event.zone_id ?? 'Zone'}</span><em>${event.event_type ?? 'Smoke'}</em><strong>${event.timestamp ? new Date(event.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : '--:--'}</strong></li>`,
                  )
                  .join('')}
              </ul>
            </div>
          </div>

          <div class="stack">
            <div class="sheet">
              <h2>Campus Map</h2>
              <div class="map-board">
                ${heatmapData
                  .map(
                    (zone, index) => `<div class="zone-chip ${zone.level}" style="left: ${10 + (index * 18)}%; top: ${20 + (index % 2) * 28}%;">${zone.zone_id}</div>`,
                  )
                  .join('')}
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
                ${heatmapData
                  .slice(0, 3)
                  .map((zone) => `<div class="heat-cell ${zone.level}">${zone.level.toUpperCase()}</div>`)
                  .join('')}
              </div>
            </div>
          </div>

          <div class="stack">
            <div class="sheet">
              <h2>Statistics</h2>
              <div class="stats-grid">
                <div class="mini-card"><span>Total</span><strong>${stats.total_events}</strong></div>
                <div class="mini-card"><span>Smoke</span><strong>${stats.smoke_events}</strong></div>
                <div class="mini-card"><span>Active</span><strong>${stats.active_cameras}</strong></div>
                <div class="mini-card"><span>Zones</span><strong>${stats.monitored_zones}</strong></div>
                <div class="mini-card"><span>Free</span><strong>${stats.smoke_free_zones}</strong></div>
                <div class="mini-card"><span>Score</span><strong>${totalSchoolScore}</strong></div>
              </div>
              <div class="chart-box">
                ${(stats.hourly ?? [])
                  .slice(0, 6)
                  .map(
                    (point) => `<div class="bar" style="height: ${(Number(point.events ?? 0) / 5) * 100}%"></div>`,
                  )
                  .join('')}
              </div>
            </div>

            <div class="sheet">
              <h2>School System</h2>
              <ul class="list-table">
                ${schoolData
                  .map(
                    (school) => `<li><span>${school.school_name}</span><strong>${school.score} points</strong><em>+${school.improvement}%</em></li>`,
                  )
                  .join('')}
              </ul>
            </div>
          </div>

          <div class="stack">
            <div class="sheet">
              <h2>Achievements</h2>
              <ul class="list-table">
                ${achievementData
                  .slice(0, 4)
                  .map((item) => `<li><span>${item.badge} ${item.title}</span><em>${item.school_id}</em></li>`)
                  .join('')}
              </ul>
            </div>
          </div>
        </section>
      </div>
    `;
  } catch (error) {
    app.innerHTML = `
      <div class="card" style="max-width: 700px; margin: 40px auto;">
        <h3>Dashboard unavailable</h3>
        <p>Unable to load AIRIS API data. Confirm the FastAPI backend is running on port 8000.</p>
        <pre>${error instanceof Error ? error.message : String(error)}</pre>
      </div>
    `;
  }
}

function renderPrivacy() {
  if (!app) return;
  app.innerHTML = `${renderNavigation('privacy')}${PrivacyView()}`;
}

function handleRoute() {
  const hash = window.location.hash.replace('#', '');
  if (hash === 'privacy') {
    renderPrivacy();
    return;
  }
  loadDashboard();
}

window.addEventListener('hashchange', handleRoute);
handleRoute();
