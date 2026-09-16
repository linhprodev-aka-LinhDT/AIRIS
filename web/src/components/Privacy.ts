export function PrivacyView(): string {
  return `
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
  `;
}
