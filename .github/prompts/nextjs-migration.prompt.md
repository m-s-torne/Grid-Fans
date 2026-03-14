# Next.js App Router Migration — Grid Fans

Migrate the existing React + Vite SPA (`frontend/`) to the Next.js 16 App Router project (`frontend_2/`). The Next.js project is already scaffolded with Tailwind CSS v4 and TypeScript.

---

## Source Project Summary

The source is a React 19 + Vite 7 SPA at `frontend/src/` with:
- **React Router v7** (client-side BrowserRouter)
- **TanStack React Query v5** for server state
- **Supabase JS v2** for auth (email/password + Google OAuth)
- **Axios** HTTP client hitting a FastAPI backend
- **Tailwind CSS v4** (via Vite plugin)
- **motion (Framer Motion v12)** for animations
- **@dnd-kit** for drag-and-drop
- **@react-three/fiber + drei + three** for 3D rendering
- **ag-grid-react** for data tables
- **chart.js + react-chartjs-2 + recharts** for charts
- **react-big-calendar + moment** for calendar views
- **react-country-flag** for flag icons
- **react-responsive** for media queries
- 5 React Contexts: Auth, Leagues, Market, ServiceProvider, TeamBuilder
- DDD-style feature folders: Auth, League, Market + core shared code

### Current Route Map

| Route | Component | Auth |
|---|---|---|
| `/` | Home (landing) | Public |
| `/login` | Login | Public (redirect if authed) |
| `/register` | Register | Public (redirect if authed) |
| `/check-email` | CheckEmail | Public |
| `/auth/confirm` | EmailConfirmation | Public |
| `/leagues` | Leagues list | Protected |
| `/leagues/:leagueId` | LeagueDetail | Protected |
| `/leagues/:leagueId/market` | Market | Protected |
| `*` | NotFound | Protected |

### Current Folder Structure (key paths)

```
frontend/src/
├── AppRouter.tsx              # All routes + provider nesting
├── main.tsx                   # Entry: StrictMode → QueryClient → BrowserRouter → AppRouter
├── index.css                  # Tailwind import, custom fonts, global styles
├── core/
│   ├── assets/                # SVG/PNG logos
│   ├── components/            # 14 shared components (GlassCard, ConfirmDialog, LoadingSpinner, etc.)
│   ├── config/
│   │   ├── axios.ts           # Axios instance + Bearer token interceptor + error interceptor
│   │   └── supabase.ts        # Supabase client creation (VITE_SUPABASE_URL, VITE_SUPABASE_ANON_KEY)
│   ├── contexts/
│   │   ├── AuthContext.tsx     # Auth state, signIn/signUp/signOut, onAuthStateChange listener
│   │   ├── LeaguesContext.tsx  # Leagues CRUD, React Query
│   │   ├── MarketContext.tsx   # Largest context: ~15 hooks, market operations, DnD state
│   │   ├── ServiceProvider.tsx # F1DataService singleton
│   │   └── TeamBuilderContext.tsx  # Team creation/editing flow
│   ├── hooks/
│   │   ├── auth/              # useAuth, useLoginForm, useRegisterForm, useEmailConfirmation
│   │   ├── db/                # useDrivers, useTeams (React Query wrappers)
│   │   ├── user/              # useBackendUser
│   │   └── userTeams/         # useUserTeam, useTeamBuilder, useMyTeamsTable
│   ├── services/
│   │   ├── env.ts             # ENV object (VITE_API_URL, VITE_SUPABASE_URL, VITE_SUPABASE_ANON_KEY, VITE_APP_URL)
│   │   ├── authService.ts     # Supabase auth wrapper
│   │   ├── backendUserService.ts  # POST /users/, GET /users/by-id/:id
│   │   ├── f1DataService.ts   # GET /drivers/, GET /teams/
│   │   ├── leagueService.ts   # Leagues CRUD endpoints
│   │   ├── marketService.ts   # Full market API (buy/sell/list/unlist/buyout)
│   │   ├── userService.ts     # Supabase direct DB queries (users table)
│   │   └── userTeamService.ts # Team CRUD + swap-reserve
│   ├── types/                 # Shared types (F1DataService, Team)
│   └── views/                 # Home.tsx, NotFound.tsx
└── features/
    ├── Auth/
    │   ├── components/        # LoginForm, RegisterForm, PublicProtectedRoute
    │   ├── views/             # Login, Register, EmailConfirmation, CheckEmail
    │   └── utils/             # authErrors.ts
    ├── League/
    │   ├── components/        # LeagueHeader, LeagueCard, LineupTab, StandingsTab, modals
    │   ├── hooks/             # useLeagueDetail, useLeagueModals, useLeagueData, etc.
    │   ├── types/             # League, CreateLeagueRequest, LineupDriver, etc.
    │   └── views/             # Leagues.tsx, LeagueDetail.tsx
    └── Market/
        ├── components/        # DriverCardExpanded, MarketHeader, MarketTabs, MarketDriverList, modals
        ├── hooks/             # useMarketState, useDriverSaleModal, useMarketHandlers/, useMarketOps/
        ├── config/            # modalConfig, modalUIConfig
        ├── types/             # marketTypes.ts
        ├── utils/             # currencyFormat, driverPricing, driverSaleCalculations, etc.
        └── views/             # Market.tsx
```

### Environment Variables (current Vite)

```
VITE_API_URL=http://localhost:8000/api
VITE_SUPABASE_URL=<supabase-project-url>
VITE_SUPABASE_ANON_KEY=<supabase-anon-key>
VITE_APP_URL=http://localhost:5173
```

---

## Migration Plan

Execute the phases below **in order**. Each phase should be fully working before moving on.

---

### Phase 0 — Install Dependencies & Configure Project

1. **Install all required packages** (use pnpm since the project already has pnpm-lock.yaml):

```bash
pnpm add @supabase/supabase-js@^2 axios @tanstack/react-query @tanstack/react-query-devtools motion @dnd-kit/core @dnd-kit/sortable @dnd-kit/utilities @react-three/fiber @react-three/drei three ag-grid-react chart.js react-chartjs-2 recharts react-big-calendar react-country-flag react-responsive moment
pnpm add -D @types/three @types/react-big-calendar
```

2. **Create `.env.local`** at `frontend_2/` root:

```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_SUPABASE_URL=<copy-from-frontend/.env>
NEXT_PUBLIC_SUPABASE_ANON_KEY=<copy-from-frontend/.env>
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

3. **Update `tsconfig.json`** — the `@/*` alias already maps to `./*`, which is correct for Next.js App Router (imports like `@/app/...`, `@/lib/...`).

4. **Copy static assets**:
   - Copy `frontend/public/fonts/` → `frontend_2/public/fonts/`
   - Copy `frontend/public/models/` → `frontend_2/public/models/`
   - Copy `frontend/public/teams/` → `frontend_2/public/teams/`
   - Copy `frontend/src/core/assets/` → `frontend_2/public/assets/` (logos)

---

### Phase 1 — Foundation Layer (lib/, config, services, types)

Create the shared infrastructure that all features depend on. Everything in this phase is non-React (no components), so there are no client/server concerns yet.

#### 1.1 Environment config

Create `frontend_2/lib/env.ts`:
- Replace all `import.meta.env.VITE_*` references with `process.env.NEXT_PUBLIC_*`
- Export an `ENV` object matching the current shape:

```ts
export const ENV = {
  API_URL: process.env.NEXT_PUBLIC_API_URL!,
  SUPABASE_URL: process.env.NEXT_PUBLIC_SUPABASE_URL!,
  SUPABASE_ANON_KEY: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
  APP_URL: process.env.NEXT_PUBLIC_APP_URL!,
};
```

#### 1.2 Supabase client

Create `frontend_2/lib/supabase.ts`:
- Copy from `frontend/src/core/config/supabase.ts`
- Replace `import.meta.env.VITE_*` with `process.env.NEXT_PUBLIC_*`
- This is a **client-side only** singleton — add `'use client'` or guard with `typeof window !== 'undefined'` if needed

#### 1.3 Axios instance

Create `frontend_2/lib/axios.ts`:
- Copy from `frontend/src/core/config/axios.ts`
- Replace `ENV.API_URL` import path
- The Bearer token interceptor must use the Supabase client from `@/lib/supabase`
- Mark as `'use client'` since it accesses browser-only Supabase session

#### 1.4 Services

Create `frontend_2/lib/services/` — copy all service files from `frontend/src/core/services/`:
- `authService.ts` → update import paths (`@/lib/supabase`)
- `backendUserService.ts` → update import paths (`@/lib/axios`)
- `f1DataService.ts` → update import paths
- `leagueService.ts` → update import paths
- `marketService.ts` → update import paths
- `userService.ts` → update import paths
- `userTeamService.ts` → update import paths
- `index.ts` → update re-exports

**Key rule**: All services use Axios or Supabase client directly. They are plain functions, not React hooks — but they run client-side only because the Axios interceptor needs the browser Supabase session for Bearer tokens.

#### 1.5 Types

Create `frontend_2/lib/types/` — copy from `frontend/src/core/types/`:
- `f1DataService.ts`
- `teamsTypes.ts`
- `index.ts`

Also copy feature-specific types:
- `frontend/src/features/League/types/leagueTypes.ts` → `frontend_2/lib/types/leagueTypes.ts`
- `frontend/src/features/Market/types/marketTypes.ts` → `frontend_2/lib/types/marketTypes.ts`

#### 1.6 Utility functions

Create `frontend_2/lib/utils/` — copy from `frontend/src/features/Market/utils/`:
- `currencyFormat.ts`
- `driverActions.ts`
- `driverNameUtils.ts`
- `driverPricing.ts`
- `driverSaleCalculations.ts`
- `modalCalculations.ts`
- `index.ts`

Also copy:
- `frontend/src/features/Auth/utils/authErrors.ts` → `frontend_2/lib/utils/authErrors.ts`

These are pure functions with no React dependency — no `'use client'` needed.

---

### Phase 2 — Global Styles & Fonts

#### 2.1 Update `app/globals.css`

Replace the content of `frontend_2/app/globals.css` with the styles from `frontend/src/index.css`:
- Keep `@import "tailwindcss";`
- Port the custom font-face declarations (Formula1 family — Regular, Bold, Black, Italic, Wide) pointing to `/fonts/`
- Port custom utilities: `shadow-solid`, `scrollbar-hide`
- Port the body gradient: dark `gray-900 → gray-800 → gray-900`
- Port AG Grid custom scrollbar styles
- Remove the default Next.js CSS variables and theme

#### 2.2 Configure fonts in layout

Update `app/layout.tsx`:
- Import Open Sans via `next/font/google` (replace Geist fonts)
- Keep Formula1 as `@font-face` in CSS (it's a local font, not available in `next/font`)
- Set metadata: `title: "Grid Fans"`, appropriate description
- Apply the dark body classes from the current `index.css`

---

### Phase 3 — Auth Infrastructure (Providers & Middleware)

This is the most critical migration piece. The current app uses React Context + React Router guards. Next.js uses middleware + server-side checks.

#### 3.1 Supabase Auth helpers

Create `frontend_2/lib/supabase-middleware.ts` (for Next.js middleware):
- Use `@supabase/supabase-js` `createClient` with cookie-based session management
- OR use `@supabase/ssr` package (install if needed: `pnpm add @supabase/ssr`) for proper cookie handling

#### 3.2 Auth Context (client-side)

Create `frontend_2/lib/contexts/AuthContext.tsx`:
- Copy from `frontend/src/core/contexts/AuthContext.tsx`
- Add `'use client'` directive at top
- Update all import paths
- Keep the `onAuthStateChange` subscription and React Query integration
- This wraps the entire app in the root layout

#### 3.3 Auth hooks

Create `frontend_2/lib/hooks/auth/`:
- Copy all files from `frontend/src/core/hooks/auth/`
- Add `'use client'` to each file
- Update import paths

#### 3.4 Next.js Middleware for route protection

Create `frontend_2/middleware.ts` at project root:
- Protect routes: `/leagues`, `/leagues/*`
- Public routes: `/`, `/login`, `/register`, `/check-email`, `/auth/confirm`
- Check for Supabase session cookie/token
- Redirect unauthenticated users to `/login`
- Redirect authenticated users away from `/login` and `/register` (PublicRoute behavior)

```ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

const publicRoutes = ['/', '/login', '/register', '/check-email', '/auth/confirm'];
const authRoutes = ['/login', '/register']; // redirect to /leagues if authed

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  // Check for Supabase auth token in cookies
  const token = request.cookies.get('sb-access-token')?.value
    || request.cookies.get('sb-<project-ref>-auth-token')?.value;

  const isAuthenticated = !!token;
  const isPublicRoute = publicRoutes.some(r => pathname === r);
  const isAuthRoute = authRoutes.some(r => pathname === r);

  if (!isAuthenticated && !isPublicRoute) {
    return NextResponse.redirect(new URL('/login', request.url));
  }
  if (isAuthenticated && isAuthRoute) {
    return NextResponse.redirect(new URL('/leagues', request.url));
  }
  return NextResponse.next();
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico|fonts|models|teams|assets).*)'],
};
```

> **Note**: Supabase cookie names vary by project. Inspect browser cookies after login to find the exact cookie name. If using `@supabase/ssr`, it handles cookies automatically.

#### 3.5 Providers wrapper

Create `frontend_2/app/providers.tsx` with `'use client'`:
- Wrap `QueryClientProvider` + `AuthProvider` + `LeaguesProvider` + `DataServiceProvider`
- This is used in `app/layout.tsx` to wrap `{children}`

```tsx
'use client';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { AuthProvider } from '@/lib/contexts/AuthContext';
import { LeaguesProvider } from '@/lib/contexts/LeaguesContext';
import { DataServiceProvider } from '@/lib/contexts/ServiceProvider';
import { useState } from 'react';

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient());
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <LeaguesProvider>
          <DataServiceProvider>
            {children}
          </DataServiceProvider>
        </LeaguesProvider>
      </AuthProvider>
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
```

Update `app/layout.tsx` to wrap children with `<Providers>`.

---

### Phase 4 — Shared Components

Create `frontend_2/components/` (or `frontend_2/lib/components/`) — copy all shared components from `frontend/src/core/components/`:

- `CustomButton.tsx` — uses `motion`, needs `'use client'`
- `DriverImage.tsx`
- `DriverInfo.tsx`
- `EmptyState.tsx`
- `EventModal.tsx`
- `ExpandButton.tsx`
- `GlassCard.tsx` — uses `motion`, needs `'use client'`
- `LoadingSpinner.tsx`
- `LoadingError.tsx`
- `TeamCreate.tsx`
- `SearchInput.tsx`
- `ConfirmDialog.tsx` — uses `motion`, needs `'use client'`
- `RandomTeamLogo.tsx` — uses Three.js, needs `'use client'`
- `index.ts`

**Rules**:
- Any component using `useState`, `useEffect`, `useContext`, `motion`, browser APIs, or event handlers needs `'use client'`
- Update all import paths from `@/core/...` to `@/components/...` or `@/lib/...`
- Replace any `<img>` tags with `next/image` `<Image>` where appropriate
- Replace any `<a>` / react-router `<Link>` with `next/link` `<Link>`

---

### Phase 5 — App Router Pages (route-by-route)

Map each React Router route to a Next.js App Router folder. Create the pages in this order:

#### 5.1 Layout with Header

Create `app/(protected)/layout.tsx`:
- This is the layout for all authenticated routes
- Renders the `Header` component (migrated from `frontend/src/layouts/Header.tsx`)
- Replace `react-router-dom` `Link` with `next/link` `Link`
- Replace `useNavigate()` with `useRouter()` from `next/navigation`
- Replace `useLocation()` with `usePathname()` from `next/navigation`
- Add `'use client'` (Header uses hooks)

#### 5.2 Public routes (no Header)

| Next.js path | Source |
|---|---|
| `app/page.tsx` | `frontend/src/core/views/Home.tsx` |
| `app/login/page.tsx` | `frontend/src/features/Auth/views/Login.tsx` |
| `app/register/page.tsx` | `frontend/src/features/Auth/views/Register.tsx` |
| `app/check-email/page.tsx` | `frontend/src/features/Auth/views/CheckEmail.tsx` |
| `app/auth/confirm/page.tsx` | `frontend/src/features/Auth/views/EmailConfirmation.tsx` |

For each:
- Add `'use client'` if the component uses hooks/state/effects
- Replace `react-router-dom` imports: `useNavigate` → `useRouter`, `useSearchParams` → `useSearchParams` from `next/navigation`, `Link` → `next/link`
- Update all internal import paths

#### 5.3 Protected routes (with Header)

| Next.js path | Source |
|---|---|
| `app/(protected)/leagues/page.tsx` | `frontend/src/features/League/views/Leagues.tsx` |
| `app/(protected)/leagues/[leagueId]/page.tsx` | `frontend/src/features/League/views/LeagueDetail.tsx` |
| `app/(protected)/leagues/[leagueId]/market/page.tsx` | `frontend/src/features/Market/views/Market.tsx` |

For each:
- Dynamic route params: `useParams()` from `next/navigation` returns `{ leagueId: string }` — same as react-router
- The Market page wraps in `MarketProvider` — move this to a `market/layout.tsx` or keep it in the page component

#### 5.4 Not Found page

Create `app/not-found.tsx` — Next.js has built-in 404 handling. Copy from `frontend/src/core/views/NotFound.tsx`, replace `Link` with `next/link`.

---

### Phase 6 — Feature Components & Hooks

Copy feature-specific components and hooks, updating them for Next.js.

#### 6.1 Auth feature

Create `frontend_2/features/Auth/`:
- Copy `components/LoginForm.tsx`, `RegisterForm.tsx` — add `'use client'`, update router imports
- The `ProtectedRoute` and `PublicRoute` components are **no longer needed** — middleware handles this
- Copy form hooks (`useLoginForm.ts`, `useRegisterForm.ts`, `useEmailConfirmation.ts`) — add `'use client'`, update imports

#### 6.2 League feature

Create `frontend_2/features/League/`:
- Copy all `components/` — add `'use client'` to interactive ones
- Copy all `hooks/` — add `'use client'`, update imports
- Replace `useNavigate` → `useRouter`, `useParams` → `useParams` (from `next/navigation`)

#### 6.3 Market feature

Create `frontend_2/features/Market/`:
- Copy all `components/`, `hooks/`, `config/`
- All interactive components need `'use client'`
- The DnD components (`DraggableCard`, `DraggableReserveSlot`) must be client components
- Charts (`DriverStatsCharts`) must be client components
- Modal components must be client components

#### 6.4 Remaining Contexts

Copy and update:
- `LeaguesContext.tsx` → `frontend_2/lib/contexts/LeaguesContext.tsx`
- `MarketContext.tsx` → `frontend_2/lib/contexts/MarketContext.tsx`  
- `ServiceProvider.tsx` → `frontend_2/lib/contexts/ServiceProvider.tsx`
- `TeamBuilderContext.tsx` → `frontend_2/lib/contexts/TeamBuilderContext.tsx`

All contexts need `'use client'`.

#### 6.5 Remaining hooks

Copy and update all hooks from `frontend/src/core/hooks/`:
- `db/useDrivers.ts`, `db/useTeams.ts`
- `user/userProfile.ts`
- `userTeams/useUserTeam.ts`, `userTeams/useTeamBuilder.ts`, `userTeams/useMyTeamsTable.tsx`

All hooks need `'use client'`.

---

### Phase 7 — React Router → Next.js Navigation Cheat Sheet

Apply these replacements **everywhere** during the migration:

| React Router (old) | Next.js App Router (new) | Import from |
|---|---|---|
| `import { Link } from 'react-router-dom'` | `import Link from 'next/link'` | `next/link` |
| `import { useNavigate } from 'react-router-dom'` | `import { useRouter } from 'next/navigation'` | `next/navigation` |
| `navigate('/path')` | `router.push('/path')` | — |
| `navigate(-1)` | `router.back()` | — |
| `import { useParams } from 'react-router-dom'` | `import { useParams } from 'next/navigation'` | `next/navigation` |
| `import { useLocation } from 'react-router-dom'` | `import { usePathname } from 'next/navigation'` | `next/navigation` |
| `location.pathname` | `pathname` (from `usePathname()`) | — |
| `import { useSearchParams } from 'react-router-dom'` | `import { useSearchParams } from 'next/navigation'` | `next/navigation` |
| `<img src="/path">` | `<Image src="/path" alt="" width={} height={} />` | `next/image` (optional — `<img>` still works) |

---

### Phase 8 — Final Integration & Cleanup

1. **Remove react-router-dom entirely** — it should not be installed in `frontend_2`

2. **Verify `next.config.ts`** — add if needed:
```ts
const nextConfig: NextConfig = {
  reactCompiler: true,
  images: {
    remotePatterns: [
      // Add any external image domains used (Supabase storage, etc.)
    ],
  },
};
```

3. **Test all routes**:
   - `/` — Landing page loads
   - `/login` — Login form works, Google OAuth redirects correctly
   - `/register` — Registration flow + email verification
   - `/leagues` — Protected, shows leagues list, create/join works
   - `/leagues/:id` — League detail with lineup/standings tabs
   - `/leagues/:id/market` — Full market with buy/sell/list/DnD
   - Unauthenticated access to protected routes redirects to `/login`
   - Authenticated access to `/login` redirects to `/leagues`

4. **Check for hydration errors** — common causes:
   - Components using `window`, `localStorage`, or `document` without `'use client'` or `useEffect` guards
   - Date formatting differences between server/client (moment.js)
   - Supabase client accessing cookies/localStorage during SSR

5. **Verify environment variables** work at build time and runtime:
   - `NEXT_PUBLIC_*` vars are inlined at build time
   - They must be set in `.env.local` AND in deployment environment

---

## Important Migration Rules

### `'use client'` Directive
- **MUST** add to any file that uses: `useState`, `useEffect`, `useContext`, `useRef`, `useCallback`, `useMemo`, `useReducer`, event handlers (`onClick`, `onChange`), browser APIs (`window`, `document`, `localStorage`), `motion` components, or any third-party client library hooks
- **DO NOT** add to: pure type files, utility functions without React imports, server components, layout files that only compose children
- When in doubt, add it — it's safe to over-mark as client, but missing it causes runtime errors

### Import Path Updates
- Old: `@/core/...`, `@/features/...` (Vite `@` → `src/`)
- New: `@/lib/...`, `@/features/...`, `@/components/...` (Next.js `@` → project root)
- Every single import must be audited and updated

### No `import.meta.env`
- Vite uses `import.meta.env.VITE_*`
- Next.js uses `process.env.NEXT_PUBLIC_*`
- Search and replace ALL occurrences

### Image Handling
- `<img>` tags still work but `next/image` `<Image>` is preferred for optimization
- Static images in `public/` are served from `/` (same as Vite)
- Imported images (`import logo from './logo.svg'`) work differently in Next.js — use `public/` folder instead or `next/image` static imports

### Framer Motion / motion
- The `motion` package works in Next.js but components using it MUST be client components
- `AnimatePresence` requires `'use client'`
- Page transitions need to be rethought (no `<Routes>` wrapper) — consider layout-level animations

### Three.js / React Three Fiber
- Must be loaded with `dynamic(() => import(...), { ssr: false })` from `next/dynamic`
- Three.js cannot run on the server — always disable SSR for these components

### AG Grid
- Must be a client component with `'use client'`
- Works the same as in Vite

---

## Target Folder Structure

```
frontend_2/
├── app/
│   ├── globals.css
│   ├── layout.tsx              # Root layout: fonts, metadata, <Providers>
│   ├── providers.tsx           # 'use client' — QueryClient + Auth + Leagues + DataService
│   ├── page.tsx                # Home (landing)
│   ├── not-found.tsx           # 404
│   ├── login/page.tsx
│   ├── register/page.tsx
│   ├── check-email/page.tsx
│   ├── auth/confirm/page.tsx
│   └── (protected)/
│       ├── layout.tsx          # Header + auth guard UI
│       └── leagues/
│           ├── page.tsx        # Leagues list
│           └── [leagueId]/
│               ├── page.tsx    # League detail
│               └── market/
│                   ├── layout.tsx  # MarketProvider wrapper (optional)
│                   └── page.tsx    # Market view
├── components/                 # Shared UI components (migrated from core/components)
├── features/
│   ├── Auth/components/        # LoginForm, RegisterForm
│   ├── League/
│   │   ├── components/
│   │   └── hooks/
│   └── Market/
│       ├── components/
│       ├── hooks/
│       ├── config/
│       └── utils/              # (or keep in lib/utils/)
├── lib/
│   ├── env.ts
│   ├── supabase.ts
│   ├── axios.ts
│   ├── contexts/               # All React contexts
│   ├── hooks/                  # All shared hooks
│   ├── services/               # All API services
│   ├── types/                  # All shared types
│   └── utils/                  # All utility functions
├── middleware.ts                # Route protection
└── public/
    ├── fonts/
    ├── models/
    ├── teams/
    └── assets/
```
