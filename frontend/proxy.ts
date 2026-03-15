import { type NextRequest, NextResponse } from 'next/server'
import { createSupabaseMiddlewareClient } from '@/lib/supabase-middleware'

const publicRoutes = ['/', '/login', '/register', '/check-email', '/auth/confirm']
const authRoutes = ['/login', '/register']

export async function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl
  const { supabase, response } = createSupabaseMiddlewareClient(request)

  const { data: { user } } = await supabase.auth.getUser()
  const isAuthenticated = !!user

  const isPublicRoute = publicRoutes.some(r => pathname === r)
  const isAuthRoute = authRoutes.some(r => pathname === r)

  if (!isAuthenticated && !isPublicRoute) {
    const url = request.nextUrl.clone()
    url.pathname = '/login'
    return NextResponse.redirect(url)
  }

  if (isAuthenticated && isAuthRoute) {
    const url = request.nextUrl.clone()
    url.pathname = '/leagues'
    return NextResponse.redirect(url)
  }

  return response
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico|fonts|models|teams|assets).*)'],
}
