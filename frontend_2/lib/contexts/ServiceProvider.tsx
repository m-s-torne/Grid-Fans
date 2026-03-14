'use client'

import { useContext, createContext } from 'react'
import type { PropsWithChildren } from 'react'
import type { F1DataService } from '@/lib/types'
import { f1DataService } from '@/lib/services'

const Ctx = createContext<F1DataService | null>(null);

export default function DataServiceProvider({ children }: PropsWithChildren) {
    return <Ctx.Provider value={f1DataService}>{children}</Ctx.Provider>
}

export function useDataService(): F1DataService {
    const val = useContext(Ctx);
    if (!val) throw new Error("useDataService function must be called inside its context provider")
    return val;
}
