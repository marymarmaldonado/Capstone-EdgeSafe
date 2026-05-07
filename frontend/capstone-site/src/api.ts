const BASE_URL = import.meta.env.VITE_API_BASE_URL;

function getToken(): string | null {
  return localStorage.getItem("token");
}

export async function apiFetch(
  path: string,
  options: RequestInit = {}
): Promise<Response> {
  const token = getToken();
  return fetch(`${BASE_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  });
}

export function logout(): void {
  localStorage.removeItem("token");
}

export function isAuthenticated(): boolean {
  return localStorage.getItem("token") !== null;
}