import { useMutation, useQueryClient } from '@tanstack/react-query';
import { userTeamService } from '@/lib/services/userTeamService';

export const useSwapReserveDriver = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ leagueId, driverId }: { leagueId: number; driverId: number }) =>
      userTeamService.swapReserveDriver(leagueId, driverId),
    
    onMutate: async (variables) => {
      const { leagueId, driverId } = variables;
      
      await queryClient.cancelQueries({ queryKey: ['user-team', leagueId] });
      await queryClient.cancelQueries({ queryKey: ['user-drivers', leagueId] });
      
      const previousTeam = queryClient.getQueryData(['user-team', leagueId]);
      const previousDrivers = queryClient.getQueryData(['user-drivers', leagueId]);
      
      queryClient.setQueryData(['user-team', leagueId], (old: any) => {
        if (!old) return old;
        
        let currentReserve = old.reserve_driver_id;
        let updatedTeam = { ...old };
        
        if (old.driver_1_id === driverId) {
          updatedTeam.driver_1_id = currentReserve;
          updatedTeam.reserve_driver_id = driverId;
        } else if (old.driver_2_id === driverId) {
          updatedTeam.driver_2_id = currentReserve;
          updatedTeam.reserve_driver_id = driverId;
        } else if (old.driver_3_id === driverId) {
          updatedTeam.driver_3_id = currentReserve;
          updatedTeam.reserve_driver_id = driverId;
        }
        
        return updatedTeam;
      });
      
      return { previousTeam, previousDrivers };
    },
    
    onError: (_err, variables, context) => {
      if (context?.previousTeam) {
        queryClient.setQueryData(['user-team', variables.leagueId], context.previousTeam);
      }
      if (context?.previousDrivers) {
        queryClient.setQueryData(['user-drivers', variables.leagueId], context.previousDrivers);
      }
    },
    
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['user-team', variables.leagueId] });
      queryClient.invalidateQueries({ queryKey: ['user-drivers', variables.leagueId] });
      queryClient.invalidateQueries({ queryKey: ['league-detail', variables.leagueId] });
    },
  });
};
