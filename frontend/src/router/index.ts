import { createRouter, createWebHistory } from 'vue-router'

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
        }
      ]
    },
    {
      path: '/admin',
      component: () => import('../components/views/admin.vue'),
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

export default router
