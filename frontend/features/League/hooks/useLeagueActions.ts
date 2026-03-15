import { useRouter } from 'next/navigation';
import { useLeagues } from '@/lib/contexts/LeaguesContext';

export const useLeagueActions = (
    leagueId: string,
    setShowLeaveModal: (show: boolean) => void
) => {
    const router = useRouter();
    const { leaveLeague, isLeavingLeague } = useLeagues();
    
    const handleLeaveLeague = async () => {
        try {
            await leaveLeague(parseInt(leagueId));
            setShowLeaveModal(false);
            router.replace('/leagues/');
        } catch (error) {
            console.error('Error leaving league:', error);
        }
    };
    
    const navigateToMarket = () => {
        router.push(`/leagues/${leagueId}/market`);
    };
    
    return {
        handleLeaveLeague,
        isLeavingLeague,
        navigateToMarket,
    };
};
