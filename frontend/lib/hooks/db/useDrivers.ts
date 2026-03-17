'use client'

import { useQuery } from '@tanstack/react-query'
import { useDataService } from '@/lib/contexts/ServiceProvider'
import { useAuth } from '@/lib/contexts/AuthContext'
import type { Driver } from '@/lib/types/marketTypes';

export const useDrivers = () => {
    const dataService = useDataService();
    const { isInitialized } = useAuth();

    return useQuery<Driver[]>({
        queryKey: ["drivers"],
        queryFn: () => dataService.getAllDrivers(),
        staleTime: 5 * 24 * 60 * 60 * 1000,
        enabled: isInitialized,
    });
}
