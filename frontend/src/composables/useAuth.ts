import { computed, reactive } from 'vue'
import {
  getCognitoConfig,
  getCognitoLoginUrl,
  getCognitoLogoutUrl,
  exchangeCodeForTokens,
  parseJwt,
  generateCodeVerifier,
  generateCodeChallenge
} from '../lib/cognito'

interface CognitoUser {
  sub: string
  email?: string
  name?: string
  picture?: string
  'custom:admin'?: boolean
  'custom:permissions'?: string
}

interface AuthState {
  user: CognitoUser | null
  accessToken: string | null
  isReady: boolean
  isAdmin: boolean
  error: string | null
}

const STORAGE_KEY_ACCESS = 'cognito_access_token'
const STORAGE_KEY_REFRESH = 'cognito_refresh_token'
const STORAGE_KEY_VERIFIER = 'cognito_code_verifier'
const STORAGE_KEY_STATE = 'cognito_state'

const state = reactive<AuthState>({
  user: null,
  accessToken: null,
  isReady: false,
  isAdmin: false,
  error: null
})

let initialization: Promise<void> | null = null

function loadTokensFromStorage(): { accessToken: string | null; refreshToken: string | null } {
  return {
    accessToken: sessionStorage.getItem(STORAGE_KEY_ACCESS),
    refreshToken: localStorage.getItem(STORAGE_KEY_REFRESH)
  }
}

function saveTokens(accessToken: string, refreshToken?: string): void {
  sessionStorage.setItem(STORAGE_KEY_ACCESS, accessToken)
  if (refreshToken) {
    localStorage.setItem(STORAGE_KEY_REFRESH, refreshToken)
  }
}

function clearTokens(): void {
  sessionStorage.removeItem(STORAGE_KEY_ACCESS)
  localStorage.removeItem(STORAGE_KEY_REFRESH)
  localStorage.removeItem(STORAGE_KEY_VERIFIER)
  localStorage.removeItem(STORAGE_KEY_STATE)
}

function decodeAccessToken(token: string): CognitoUser {
  const payload = parseJwt(token)
  return {
    sub: payload.sub as string,
    email: payload.email as string | undefined,
    name: payload.name as string | undefined,
    picture: payload.picture as string | undefined,
    'custom:admin': payload['custom:admin'] as boolean | undefined,
    'custom:permissions': payload['custom:permissions'] as string | undefined
  }
}

export function initializeAuth(): Promise<void> {
  if (initialization) return initialization

  initialization = new Promise((resolve) => {
    const { accessToken } = loadTokensFromStorage()

    if (accessToken) {
      try {
        const user = decodeAccessToken(accessToken)
        const exp = parseJwt(accessToken).exp as number | undefined
        const isExpired = exp ? exp * 1000 < Date.now() : true

        if (isExpired) {
          clearTokens()
          state.user = null
          state.accessToken = null
          state.isAdmin = false
        } else {
          state.user = user
          state.accessToken = accessToken
          state.isAdmin = user['custom:admin'] === true
        }
      } catch {
        clearTokens()
        state.user = null
        state.accessToken = null
        state.isAdmin = false
      }
    }

    state.isReady = true
    resolve()
  })

  return initialization
}

export async function loginWithCognito(): Promise<void> {
  state.error = null
  const verifier = generateCodeVerifier()
  const challenge = await generateCodeChallenge(verifier)
  const stateParam = crypto.randomUUID()

  localStorage.setItem(STORAGE_KEY_VERIFIER, verifier)
  localStorage.setItem(STORAGE_KEY_STATE, stateParam)

  const url = getCognitoLoginUrl(challenge, stateParam)
  window.location.href = url
}

export async function handleCallback(code: string, stateParam: string): Promise<boolean> {
  const savedState = localStorage.getItem(STORAGE_KEY_STATE)
  if (savedState !== stateParam) {
    state.error = 'Invalid state parameter'
    return false
  }

  const verifier = localStorage.getItem(STORAGE_KEY_VERIFIER)
  if (!verifier) {
    state.error = 'Code verifier not found'
    return false
  }

  try {
    const tokens = await exchangeCodeForTokens(code)
    saveTokens(tokens.access_token, tokens.refresh_token)

    const user = decodeAccessToken(tokens.access_token)
    state.user = user
    state.accessToken = tokens.access_token
    state.isAdmin = user['custom:admin'] === true

    clearTokens()
    return true
  } catch (error) {
    state.error = error instanceof Error ? error.message : 'Login failed'
    return false
  }
}

export async function logout(): Promise<void> {
  clearTokens()
  state.user = null
  state.accessToken = null
  state.isAdmin = false

  const url = getCognitoLogoutUrl()
  window.location.href = url
}

export function getAccessToken(): string | null {
  return state.accessToken
}

export function useAuth() {
  return {
    state,
    user: computed(() => state.user),
    isReady: computed(() => state.isReady),
    isAuthenticated: computed(() => state.user !== null),
    isAdmin: computed(() => state.isAdmin),
    loginWithCognito,
    logout
  }
}

export { state as authState }
