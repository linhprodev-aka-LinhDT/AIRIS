export function Dashboard(): string {
  return `
    <div class="dashboard">
      <header class="header">
        <div>
          <h1>AIRIS</h1>
          <div class="subtitle">Smoke-Free Campus</div>
        </div>
        <div class="badge">DEMO MODE</div>
      </header>

      <section class="system-status">
        <article class="card">
          <h3>Cameras Online</h3>
          <p class="metric">12</p>
        </article>
        <article class="card">
          <h3>Active Zones</h3>
          <p class="metric">18</p>
        </article>
        <article class="card">
          <h3>Events Today</h3>
          <p class="metric">14</p>
        </article>
        <article class="card">
          <h3>Smoke-Free Zones</h3>
          <p class="metric">13</p>
        </article>
      </section>

      <section class="grid">
        <article class="card map-panel">
          <h3>Campus Map</h3>
          <div class="map-box">
            <div class="zone zone-low" style="left: 8%; top: 18%;">Zone A</div>
            <div class="zone zone-medium" style="left: 40%; top: 30%;">Zone B</div>
            <div class="zone zone-high" style="left: 66%; top: 48%;">Zone C</div>
            <div class="zone zone-low" style="left: 28%; top: 72%;">Zone D</div>
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
            <li><span>Zone A</span><span>Smoke Event</span><span>10:32</span></li>
            <li><span>Zone C</span><span>Smoking Behavior</span><span>11:04</span></li>
            <li><span>Zone D</span><span>Smoke Event</span><span>12:16</span></li>
          </ul>
        </article>
      </section>

      <section class="grid" style="margin-top: 20px;">
        <article class="card">
          <h3>School Score</h3>
          <ul class="score-list">
            <li><span>School A</span><strong>245 points</strong></li>
            <li><span>School B</span><strong>198 points</strong></li>
          </ul>
        </article>

        <article class="card">
          <h3>Achievements</h3>
          <ul class="achievement-list">
            <li><strong>🏆 Smoke-Free Zone</strong></li>
            <li><strong>🏆 7 Days Improvement</strong></li>
            <li><strong>🏆 High Monitoring Coverage</strong></li>
          </ul>
        </article>
      </section>
    </div>
  `;
}
