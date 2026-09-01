import { computed, reactive } from 'vue'
import {
  GoogleAuthProvider,
  getIdToken,
  getIdTokenResult,
  onAuthStateChanged,
  signInWithPopup,
  signOut,
  type User
} from 'firebase/auth'
import { firebaseAuth } from '../lib/firebase'

interface AuthState {
  user: User | null
  isReady: boolean
  isAdmin: boolean
  error: string | null
}

const state = reactive<AuthState>({
  user: null,
  isReady: false,
  isAdmin: false,
  error: null
})

let initialization: Promise<void> | null = null

export function initializeAuth(): Promise<void> {
  if (initialization) return initialization

  initialization = new Promise((resolve) => {
    onAuthStateChanged(
      firebaseAuth,
      async (user) => {
        state.user = user
        state.error = null

        if (user) {
          const token = await getIdTokenResult(user)
          state.isAdmin = token.claims.admin === true
        } else {
          state.isAdmin = false
        }

        state.isReady = true
        resolve()
      },
      (error) => {
        state.error = error.message
        state.isReady = true
        resolve()
      }
    )
  })

  return initialization
}

export async function loginWithGoogle(): Promise<void> {
  state.error = null
  const provider = new GoogleAuthProvider()
  provider.setCustomParameters({ prompt: 'select_account' })
  await signInWithPopup(firebaseAuth, provider)
}

export async function logout(): Promise<void> {
  await signOut(firebaseAuth)
}

export async function getFirebaseToken(forceRefresh = false): Promise<string | null> {
  if (!firebaseAuth.currentUser) return null
  return getIdToken(firebaseAuth.currentUser, forceRefresh)
}

export function useAuth() {
  return {
    state,
    user: computed(() => state.user),
    isReady: computed(() => state.isReady),
    isAuthenticated: computed(() => state.user !== null),
    isAdmin: computed(() => state.isAdmin),
    loginWithGoogle,
    logout
  }
}

export { state as authState }
