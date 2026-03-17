'use client'

import { useDataService } from '@/lib/contexts/ServiceProvider'
import { useQuery } from '@tanstack/react-query'
import { useAuth } from '@/lib/contexts/AuthContext'
import type { Team } from '@/lib/types/teamsTypes'

export const useTeams = () => {
    const dataService = useDataService();
    const { isInitialized } = useAuth();

    return useQuery<Team[]>({
        queryKey: ['teams'],
        queryFn: () => dataService.getAllTeams(),
        staleTime: 5 * 24 * 60 * 60 * 1000,
        enabled: isInitialized,
    })
}
