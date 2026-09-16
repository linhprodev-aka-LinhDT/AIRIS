import type { Achievement, Camera, EventSummary, HeatmapPoint, School, Statistics, Zone } from '../types/api';

const API_BASE = '/api';

async function getJson<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`);
  if (!response.ok) {
    throw new Error(`API request failed: ${response.status} ${response.statusText}`);
  }
  return response.json() as Promise<T>;
}

export const api = {
  health: () => getJson<{ status: string; demo_mode: boolean; timestamp: string }>('/health'),
  schools: () => getJson<{ schools: School[] }>('/schools'),
  school: (schoolId: string) => getJson<{ school: School }>(`/schools/${schoolId}`),
  zones: () => getJson<{ zones: Zone[] }>('/zones'),
  zone: (zoneId: string) => getJson<{ zone: Zone }>(`/zones/${zoneId}`),
  events: () => getJson<{ events: EventSummary[] }>('/events'),
  statistics: () => getJson<Statistics>('/statistics'),
  heatmap: () => getJson<{ zones: HeatmapPoint[] }>('/heatmap'),
  leaderboard: () => getJson<{ leaderboard: Array<{ school_id: string; school_name: string; score: number; improvement: number; coverage: number }> }>('/leaderboard'),
  achievements: () => getJson<{ achievements: Achievement[] }>('/achievements'),
  cameras: () => getJson<{ cameras: Camera[] }>('/cameras'),
  camera: (cameraId: string) => getJson<{ camera: Camera }>(`/cameras/${cameraId}`),
};
