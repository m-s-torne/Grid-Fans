import { createContext, useContext, type ReactNode } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { leagueService, type League, type CreateLeagueRequest, type JoinLeagueRequest, type JoinLeagueResponse } from '@/core/services'
import { useAuth } from '@/core/contexts/AuthContext'

type LeaguesContextType = {
  // Queries
  leagues: League[]
  isLoading: boolean
  error: Error | null
  
  // Mutations
  createLeague: (leagueData: CreateLeagueRequest) => Promise<League>
  joinLeague: (joinData: JoinLeagueRequest) => Promise<JoinLeagueResponse>
  leaveLeague: (leagueId: number) => Promise<{ message: string; league_id: number }>
  
  // Utilities
  refetchLeagues: () => void
  isCreatingLeague: boolean
  isJoiningLeague: boolean
  isLeavingLeague: boolean
}

const LeaguesContext = createContext<LeaguesContextType | null>(null)

export const useLeagues = () => {
  const context = useContext(LeaguesContext)
  if (!context) {
    throw new Error('useLeagues must be used within LeaguesProvider')
  }
  return context
}

export const LeaguesProvider = ({ children }: { children: ReactNode }) => {
  const { user } = useAuth()
  const queryClient = useQueryClient()
  
  // Query para obtener ligas del usuario
  const { data: leagues = [], isLoading, error, refetch } = useQuery({
    queryKey: ['leagues', user?.id],
    queryFn: () => leagueService.getUserLeagues(),
    enabled: !!user?.id,
    staleTime: 5 * 60 * 1000, // 5 minutos
    placeholderData: (previousData) => previousData, // Mantener datos anteriores durante refetch
  })

  // Mutation para crear liga
  const createLeagueMutation = useMutation({
    mutationFn: (leagueData: CreateLeagueRequest) => 
      leagueService.createLeague(leagueData),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['leagues', user?.id] })
    }
  })

  // Mutation para unirse a liga
  const joinLeagueMutation = useMutation({
    mutationFn: (joinData: JoinLeagueRequest) => 
      leagueService.joinLeague(joinData),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['leagues', user?.id] })
    }
  })

  // Mutation para abandonar liga
  const leaveLeagueMutation = useMutation({
    mutationFn: (leagueId: number) => 
      leagueService.leaveLeague(leagueId),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['leagues', user?.id] })
      // También invalidar el equipo del usuario para esa liga específica
      queryClient.invalidateQueries({ queryKey: ['userTeam', data.league_id, user?.id] })
    }
  })

  return (
    <LeaguesContext.Provider value={{
      leagues,
      isLoading,
      error,
      createLeague: createLeagueMutation.mutateAsync,
      joinLeague: joinLeagueMutation.mutateAsync,
      leaveLeague: leaveLeagueMutation.mutateAsync,
      refetchLeagues: refetch,
      isCreatingLeague: createLeagueMutation.isPending,
      isJoiningLeague: joinLeagueMutation.isPending,
      isLeavingLeague: leaveLeagueMutation.isPending
    }}>
      {children}
    </LeaguesContext.Provider>
  )
}