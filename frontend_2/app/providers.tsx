'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { AuthProvider } from '@/lib/contexts/AuthContext';
import { LeaguesProvider } from '@/lib/contexts/LeaguesContext';
import DataServiceProvider from '@/lib/contexts/ServiceProvider';
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
