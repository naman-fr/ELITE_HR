const DEFAULT_API_BASE = '';

export function getApiBaseUrl(): string {
  const configured = process.env.NEXT_PUBLIC_API_URL?.trim();
  if (!configured) {
    return DEFAULT_API_BASE;
  }
  return configured.replace(/\/$/, '');
}

export function apiUrl(path: string): string {
  const base = getApiBaseUrl();
  const normalizedPath = path.startsWith('/') ? path : `/${path}`;
  return `${base}${normalizedPath}`;
}

export async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(apiUrl(path), init);
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || `Request failed with status ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export interface DashboardStats {
  headcount: number;
  avg_productivity: number;
  compliance_risks: number;
  identity_health: number;
  departments: { label: string; val: number }[];
}

export interface KeycloakStatus {
  status: string;
  connected: boolean;
  total_users?: number;
  mfa_compliance?: number;
  users?: { username: string; email: string; enabled: boolean; totp: boolean }[];
  error?: string;
}

export interface WazuhAlert {
  name: string;
  device: string;
  risk: string;
  status?: string;
  source?: string;
}

export interface WazuhStatus {
  status: string;
  connected: boolean;
  total_agents?: number;
  safe_agents?: number;
  alerts?: WazuhAlert[];
  error?: string;
}

export interface ComplianceAlerts {
  total: number;
  alerts: WazuhAlert[];
}
