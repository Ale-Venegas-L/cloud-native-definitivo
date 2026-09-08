import { describe, it, expect } from 'vitest'
import router from '@/router'

describe('Router', () => {
  it('has home route', () => {
    const route = router.getRoutes().find((r) => r.path === '/')
    expect(route).toBeDefined()
  })

  it('has books route', () => {
    const route = router.getRoutes().find((r) => r.path === '/books')
    expect(route).toBeDefined()
  })

  it('has admin route', () => {
    const route = router.getRoutes().find((r) => r.path === '/admin')
    expect(route).toBeDefined()
  })

  it('has admin stock route', () => {
    const route = router.getRoutes().find((r) => r.path === '/admin/stock')
    expect(route).toBeDefined()
  })

  it('has 4 routes total', () => {
    const routes = router.getRoutes()
    expect(routes.length).toBe(4)
  })
})
