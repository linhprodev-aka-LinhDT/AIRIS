export function Heatmap(): string {
  return `
    <div class="sheet">
      <h2>Smoke Heatmap</h2>
      <div class="heat-grid">
        <div class="heat-cell low">Low</div>
        <div class="heat-cell medium">Medium</div>
        <div class="heat-cell high">High</div>
      </div>
    </div>
  `;
}
