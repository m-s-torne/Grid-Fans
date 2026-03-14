import { useQuery } from '@tanstack/react-query';
import { leagueService } from '@/core/services';
import { useAuth } from '@/core/contexts/AuthContext';
import { useUserTeam } from '@/core/hooks/userTeams/useUserTeam';
import { useDrivers } from '@/core/hooks/db/useDrivers';
import { useTeams } from '@/core/hooks/db/useTeams';
import { useUserDrivers } from '@/features/Market/hooks/useMarketOps';

/**
 * Hook: Fetch all league-related data
 * Responsibility: Data fetching only
 */
export const useLeagueData = (leagueId: string | undefined) => {
    const { user } = useAuth();
    
    const leagueQuery = useQuery({
        queryKey: ['league-detail', leagueId, user?.id],
        queryFn: () => leagueService.getLeagueById(parseInt(leagueId!)),
        enabled: !!leagueId && !!user?.id,
        staleTime: 5 * 60 * 1000,
        retry: 1,
    });
    
    const { data: userTeam, isLoading: teamLoading } = useUserTeam(parseInt(leagueId!));
    const { data: allDrivers } = useDrivers();
    const { data: allTeams } = useTeams();
    const { data: myDriversWithOwnership } = useUserDrivers(
        parseInt(leagueId!),
        user?.id || ''
    );
    
    return {
        league: leagueQuery.data,
        isLoading: leagueQuery.isLoading,
        error: leagueQuery.error,
        userTeam,
        teamLoading,
        allDrivers,
        allTeams,
        myDriversWithOwnership,
    };
};