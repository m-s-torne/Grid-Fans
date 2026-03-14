import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { userTeamService } from '@/core/services';
import type { CreateUserTeamRequest } from '@/core/services';
import { useAuth } from '@/core/contexts/AuthContext';

export const useUserTeam = (leagueId: number) => {
    const { user } = useAuth();
    
    return useQuery({
        queryKey: ['user-team', leagueId, user?.id],
        queryFn: () => userTeamService.getMyTeam(leagueId),
        enabled: !!leagueId && !!user?.id,
        staleTime: 5 * 60 * 1000, // 5 minutos
    });
};

export const useCreateOrUpdateTeam = () => {
    const { user } = useAuth();
    const queryClient = useQueryClient();
    
    return useMutation({
        mutationFn: ({ leagueId, teamData }: { leagueId: number; teamData: CreateUserTeamRequest }) =>
            userTeamService.createOrUpdateTeam(leagueId, teamData),
        onSuccess: (_, variables) => {
            // Invalidar las queries relacionadas
            queryClient.invalidateQueries({ queryKey: ['user-team', variables.leagueId] });
            queryClient.invalidateQueries({ queryKey: ['league-detail', variables.leagueId] });
        },
    });
};