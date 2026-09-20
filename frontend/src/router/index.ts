import { createRouter, createWebHistory } from 'vue-router'
import { authState, initializeAuth } from '../composables/useAuth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: () => import('../components/views/public.vue'),
      children: [
        {
          path: '',
          name: 'home',
          component: () => import('../components/pages/public/home.vue')
        },
        {
          path: 'books',
          name: 'books',
          component: () => import('../components/pages/public/books.vue')
        },
        {
          path: 'editions',
          name: 'editions',
          component: () => import('../components/pages/public/editions.vue')
        }
      ]
    },
    {
      path: '/callback',
      name: 'callback',
      component: () => import('../components/pages/auth/callback.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../components/pages/auth/login.vue')
    },
    {
      path: '/unauthorized',
      name: 'unauthorized',
      component: () => import('../components/pages/auth/unauthorized.vue')
    },
    {
      path: '/admin',
      component: () => import('../components/views/admin.vue'),
      meta: { requiresAdmin: true },
      children: [
        {
          path: '',
          name: 'admin-panel',
          component: () => import('../components/pages/admin/panel.vue')
        },
        {
          path: 'stock',
          name: 'admin-stock',
          component: () => import('../components/pages/admin/stock.vue')
        }
      ]
    }
  ]
})

router.beforeEach(async (to) => {
  await initializeAuth()

  if (!to.meta.requiresAdmin) return true

  if (!authState.user) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }

  if (!authState.isAdmin) {
    return { name: 'unauthorized' }
  }

  return true
})

export default router
