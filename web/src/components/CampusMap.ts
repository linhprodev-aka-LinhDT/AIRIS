export function CampusMap(): string {
  return `
    <div class="sheet">
      <h2>Campus Map</h2>
      <div class="map-board">
        <div class="zone-chip low" style="left: 10%; top: 18%;">Zone A</div>
        <div class="zone-chip medium" style="left: 38%; top: 28%;">Zone B</div>
        <div class="zone-chip high" style="left: 65%; top: 50%;">Zone C</div>
        <div class="zone-chip low" style="left: 25%; top: 70%;">Zone D</div>
      </div>
      <div class="legend-row">
        <span><i class="dot low"></i> Low density</span>
        <span><i class="dot medium"></i> Medium density</span>
        <span><i class="dot high"></i> High density</span>
      </div>
    </div>
  `;
}
