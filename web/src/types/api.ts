export type School = {
  school_id: string;
  school_name: string;
  zone_count: number;
  camera_count: number;
  score: number;
  improvement: number;
  coverage: number;
  smoke_density: number;
  status: string;
  achievements: string[];
};

export type Zone = {
  zone_id: string;
  school_id: string;
  zone_name: string;
  camera_id?: string | null;
  location: Record<string, unknown>;
  event_count: number;
  smoke_density: number;
  last_event?: string | null;
  status: string;
  coverage: number;
};

export type Camera = {
  camera_id: string;
  school_id: string;
  name: string;
  zone_id?: string | null;
  status: string;
  stream_url?: string | null;
  health: number;
};

export type EventSummary = {
  event_id?: string;
  school_id?: string;
  zone_id?: string;
  camera_id?: string;
  event_type?: string;
  timestamp?: string;
  confidence?: number;
  duration?: number;
  metadata?: Record<string, unknown>;
};

export type Statistics = {
  total_events: number;
  smoke_events: number;
  smoking_behavior_events: number;
  active_cameras: number;
  monitored_zones: number;
  smoke_free_zones: number;
  hourly: Array<Record<string, number | string>>;
  daily: Array<Record<string, number | string>>;
  weekly: Array<Record<string, number | string>>;
  monthly: Array<Record<string, number | string>>;
};

export type HeatmapPoint = {
  zone_id: string;
  school_id: string;
  smoke_density: number;
  level: 'low' | 'medium' | 'high';
  event_count: number;
};

export type Achievement = {
  id: string;
  title: string;
  description: string;
  school_id: string;
  badge: string;
};

export type AirQualityReading = {
  sensor_id: string;
  zone_id: string;
  timestamp: string;
  pm25?: number | null;
  co_ppm?: number | null;
  co2_ppm?: number | null;
  voc_index?: number | null;
  smoke_alarm: boolean;
};

export type AwarenessQuestion = {
  question_id: string;
  question: string;
  options: string[];
  points: number;
};
