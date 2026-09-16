export function CameraView(): string {
  return `
    <div class="sheet">
      <h2>Camera Monitor</h2>
      <div class="toolbar">
        <select>
          <option>Camera 1 — School A</option>
          <option>Camera 2 — School A</option>
          <option>Camera 3 — School B</option>
        </select>
        <button>Start Camera</button>
        <button class="secondary">Stop Camera</button>
      </div>
      <div class="camera-stage">
        <div class="camera-placeholder">Live camera preview</div>
      </div>
      <div class="status-grid">
        <div class="mini-card"><span>AI status</span><strong>READY</strong></div>
        <div class="mini-card"><span>Detection</span><strong>SMOKE ALERT</strong></div>
        <div class="mini-card"><span>Confidence</span><strong>0.93</strong></div>
      </div>
    </div>
  `;
}
