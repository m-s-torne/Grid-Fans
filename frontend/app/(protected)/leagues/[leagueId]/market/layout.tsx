'use client';

import { MarketProvider } from '@/lib/contexts/MarketContext';

export default function MarketLayout({ children }: { children: React.ReactNode }) {
    return (
        <MarketProvider>
            {children}
        </MarketProvider>
    );
}
