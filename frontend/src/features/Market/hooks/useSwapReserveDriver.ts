import { useMutation, useQueryClient } from '@tanstack/react-query';
import { userTeamService } from '@/core/services/userTeamService';

export const useSwapReserveDriver = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ leagueId, driverId }: { leagueId: number; driverId: number }) =>
      userTeamService.swapReserveDriver(leagueId, driverId),
    
    // Optimistic update: actualizar UI inmediatamente antes de la respuesta del backend
    onMutate: async (variables) => {
      const { leagueId, driverId } = variables;
      
      // Cancelar queries en progreso para evitar que sobrescriban nuestro optimistic update
      await queryClient.cancelQueries({ queryKey: ['user-team', leagueId] });
      await queryClient.cancelQueries({ queryKey: ['user-drivers', leagueId] });
      
      // Guardar el estado actual por si necesitamos hacer rollback
      const previousTeam = queryClient.getQueryData(['user-team', leagueId]);
      const previousDrivers = queryClient.getQueryData(['user-drivers', leagueId]);
      
      // Actualizar optimísticamente el user-team
      queryClient.setQueryData(['user-team', leagueId], (old: any) => {
        if (!old) return old;
        
        // Encontrar en qué slot está el driver que queremos hacer reserve
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
      
      // Retornar el contexto para rollback si falla
      return { previousTeam, previousDrivers };
    },
    
    // Si el backend falla, revertir el optimistic update
    onError: (_err, variables, context) => {
      if (context?.previousTeam) {
        queryClient.setQueryData(['user-team', variables.leagueId], context.previousTeam);
      }
      if (context?.previousDrivers) {
        queryClient.setQueryData(['user-drivers', variables.leagueId], context.previousDrivers);
      }
    },
    
    // Solo cuando el backend responde exitosamente, invalidar para obtener datos frescos
    onSuccess: (_, variables) => {
      // Invalidate queries to refresh with server data after successful swap
      queryClient.invalidateQueries({ queryKey: ['user-team', variables.leagueId] });
      queryClient.invalidateQueries({ queryKey: ['user-drivers', variables.leagueId] });
      queryClient.invalidateQueries({ queryKey: ['league-detail', variables.leagueId] });
    },
  });
};
