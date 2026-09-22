import { getAccessToken } from '../composables/useAuth'

const apiBase = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

export class ApiError extends Error {
  constructor(
    public readonly status: number,
    message: string
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

interface RequestOptions extends RequestInit {
  authenticated?: boolean
}

async function executeRequest<T>(
  path: string,
  options: RequestOptions,
): Promise<T> {
  const headers = new Headers(options.headers)
  headers.set('Accept', 'application/json')

  if (options.body && !headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json')
  }

  if (options.authenticated) {
    const token = getAccessToken()
    if (!token) throw new ApiError(401, 'Debes iniciar sesión')
    headers.set('Authorization', `Bearer ${token}`)
  }

  const response = await fetch(`${apiBase}${path}`, { ...options, headers })

  if (!response.ok) {
    const payload = await response.json().catch(() => null) as { detail?: string } | null
    throw new ApiError(response.status, payload?.detail || 'No fue posible completar la solicitud')
  }

  if (response.status === 204) return undefined as T
  return response.json() as Promise<T>
}

export function apiRequest<T>(path: string, options: RequestOptions = {}): Promise<T> {
  return executeRequest<T>(path, options)
}
