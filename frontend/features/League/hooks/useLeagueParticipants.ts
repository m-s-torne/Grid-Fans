import { useQuery } from '@tanstack/react-query'
import { leagueService, type LeagueParticipantsResponse } from '@/lib/services'

export const useLeagueParticipants = (leagueId: number) => {
  return useQuery<LeagueParticipantsResponse>({
    queryKey: ['league-participants', leagueId],
    queryFn: () => leagueService.getLeagueParticipants(leagueId),
    enabled: !!leagueId,
    staleTime: 50 * 60 * 1000,
  })
}
