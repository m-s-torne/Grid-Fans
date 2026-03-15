import { useQuery } from '@tanstack/react-query';
import { leagueService } from '@/lib/services';
import { useAuth } from '@/lib/contexts/AuthContext';
import { useUserTeam } from '@/lib/hooks/userTeams/useUserTeam';
import { useDrivers } from '@/lib/hooks/db/useDrivers';
import { useTeams } from '@/lib/hooks/db/useTeams';
import { useUserDrivers } from '@/features/Market/hooks/useMarketOps';

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
