export function Statistics(): string {
  return `
    <div class="sheet">
      <h2>Statistics</h2>
      <div class="stats-grid">
        <div class="mini-card"><span>Total events</span><strong>14</strong></div>
        <div class="mini-card"><span>Smoke events</span><strong>9</strong></div>
        <div class="mini-card"><span>Active cameras</span><strong>4</strong></div>
        <div class="mini-card"><span>Smoke-free zones</span><strong>5</strong></div>
      </div>
      <div class="chart-box">
        <div class="bar" style="height: 35%"></div>
        <div class="bar" style="height: 55%"></div>
        <div class="bar" style="height: 70%"></div>
        <div class="bar" style="height: 45%"></div>
        <div class="bar" style="height: 88%"></div>
        <div class="bar" style="height: 62%"></div>
      </div>
    </div>
  `;
}
