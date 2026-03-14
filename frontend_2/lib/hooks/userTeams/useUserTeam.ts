'use client'

import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { userTeamService } from '@/lib/services'
import type { CreateUserTeamRequest } from '@/lib/services'
import { useAuth } from '@/lib/contexts/AuthContext'

export const useUserTeam = (leagueId: number) => {
    const { user } = useAuth();
    
    return useQuery({
        queryKey: ['user-team', leagueId, user?.id],
        queryFn: () => userTeamService.getMyTeam(leagueId),
        enabled: !!leagueId && !!user?.id,
        staleTime: 5 * 60 * 1000,
    });
};

export const useCreateOrUpdateTeam = () => {
    const queryClient = useQueryClient();
    
    return useMutation({
        mutationFn: ({ leagueId, teamData }: { leagueId: number; teamData: CreateUserTeamRequest }) =>
            userTeamService.createOrUpdateTeam(leagueId, teamData),
        onSuccess: (_, variables) => {
            queryClient.invalidateQueries({ queryKey: ['user-team', variables.leagueId] });
            queryClient.invalidateQueries({ queryKey: ['league-detail', variables.leagueId] });
        },
    });
};
