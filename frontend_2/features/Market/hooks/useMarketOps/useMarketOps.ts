/**
 * Market API hooks for driver ownership and transactions
 */
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { marketService } from '@/lib/services';
import type {
  BuyDriverFromMarketRequest,
  BuyDriverFromUserRequest,
  SellDriverToMarketRequest,
  ListDriverForSaleRequest,
  UnlistDriverRequest,
  BuyoutClauseRequest,
} from '@/features/Market/types/marketTypes';

type DriverTransactionParams = {
  leagueId: number;
  driverId: number;
}

export interface BuyFromMarketMutation extends DriverTransactionParams {
  request: BuyDriverFromMarketRequest;
}

export interface BuyFromUserMutation extends DriverTransactionParams {
  request: BuyDriverFromUserRequest;
}

export interface SellToMarketMutation extends DriverTransactionParams {
  request: SellDriverToMarketRequest
}

export interface ListForSaleMutation extends DriverTransactionParams {
  request: ListDriverForSaleRequest
}

export interface UnlistDriverMutation extends DriverTransactionParams {
  request: UnlistDriverRequest
}

/**
 * Get all driver ownerships for a league
 */
export const useDriverOwnerships = (leagueId: number) => {
  return useQuery({
    queryKey: ['driver-ownerships', leagueId],
    queryFn: () => marketService.getDriverOwnerships(leagueId),
    staleTime: 30 * 1000,
    enabled: !!leagueId,
  });
};

/**
 * Get free agent drivers in a league
 */
export const useFreeDrivers = (leagueId: number) => {
  return useQuery({
    queryKey: ['free-drivers', leagueId],
    queryFn: () => marketService.getFreeDrivers(leagueId),
    staleTime: 30 * 1000,
    enabled: !!leagueId,
  });
};

/**
 * Get drivers listed for sale in a league
 */
export const useDriversForSale = (leagueId: number) => {
  return useQuery({
    queryKey: ['drivers-for-sale', leagueId],
    queryFn: () => marketService.getDriversForSale(leagueId),
    staleTime: 30 * 1000,
    enabled: !!leagueId,
  });
};

/**
 * Get drivers owned by a specific user in a league
 */
export const useUserDrivers = (leagueId: number, userId: number | string) => {
  return useQuery({
    queryKey: ['user-drivers', leagueId, userId],
    queryFn: () => marketService.getUserDrivers(leagueId, userId),
    staleTime: 30 * 1000,
    enabled: !!leagueId && !!userId,
  });
};

/**
 * Buy a driver from the market (free agent)
 */
export const useBuyFromMarket = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ leagueId, driverId, request }: BuyFromMarketMutation) => marketService.buyDriverFromMarket(leagueId, driverId, request),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['driver-ownerships', variables.leagueId] });
      queryClient.invalidateQueries({ queryKey: ['free-drivers', variables.leagueId] });
      queryClient.invalidateQueries({ queryKey: ['user-drivers', variables.leagueId] });
      queryClient.invalidateQueries({ queryKey: ['user-team', variables.leagueId], exact: false });
      queryClient.invalidateQueries({ queryKey: ['league-detail', variables.leagueId], exact: false });
    },
  });
};

/**
 * Buy a driver from another user
 */
export const useBuyFromUser = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ leagueId, driverId, request }: BuyFromUserMutation) => marketService.buyDriverFromUser(leagueId, driverId, request),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['driver-ownerships', variables.leagueId] });
      queryClient.invalidateQueries({ queryKey: ['drivers-for-sale', variables.leagueId] });
      queryClient.invalidateQueries({ queryKey: ['user-drivers', variables.leagueId] });
      queryClient.invalidateQueries({ queryKey: ['user-team', variables.leagueId], exact: false });
      queryClient.invalidateQueries({ queryKey: ['league-detail', variables.leagueId], exact: false });
    },
  });
};

/**
 * Sell a driver to the market (quick sell)
 */
export const useSellToMarket = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ leagueId, driverId, request }: SellToMarketMutation) => marketService.sellDriverToMarket(leagueId, driverId, request),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['driver-ownerships', variables.leagueId] });
      queryClient.invalidateQueries({ queryKey: ['free-drivers', variables.leagueId] });
      queryClient.invalidateQueries({ queryKey: ['user-drivers', variables.leagueId] });
      queryClient.invalidateQueries({ queryKey: ['user-team', variables.leagueId], exact: false });
      queryClient.invalidateQueries({ queryKey: ['league-detail', variables.leagueId], exact: false });
    },
  });
};

/**
 * List a driver for sale
 */
export const useListForSale = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ leagueId, driverId, request }: ListForSaleMutation) => marketService.listDriverForSale(leagueId, driverId, request),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['driver-ownerships', variables.leagueId] });
      queryClient.invalidateQueries({ queryKey: ['drivers-for-sale', variables.leagueId] });
      queryClient.invalidateQueries({ queryKey: ['user-drivers', variables.leagueId] });
    },
  });
};

/**
 * Remove a driver from sale listings
 */
export const useUnlistFromSale = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ leagueId, driverId, request }: UnlistDriverMutation) => marketService.unlistDriverFromSale(leagueId, driverId, request),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['driver-ownerships', variables.leagueId] });
      queryClient.invalidateQueries({ queryKey: ['drivers-for-sale', variables.leagueId] });
      queryClient.invalidateQueries({ queryKey: ['user-drivers', variables.leagueId] });
    },
  });
};

/**
 * Execute a buyout clause
 */
export const useBuyoutClause = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ leagueId, driverId, request }: {
      leagueId: number;
      driverId: number;
      request: BuyoutClauseRequest;
    }) => marketService.executeBuyoutClause(leagueId, driverId, request),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['driver-ownerships', variables.leagueId] });
      queryClient.invalidateQueries({ queryKey: ['user-drivers', variables.leagueId] });
      queryClient.invalidateQueries({ queryKey: ['user-team', variables.leagueId], exact: false });
      queryClient.invalidateQueries({ queryKey: ['league-detail', variables.leagueId], exact: false });
    },
  });
};

/**
 * Get market transactions history
 */
export const useMarketTransactions = (leagueId: number) => {
  return useQuery({
    queryKey: ['market-transactions', leagueId],
    queryFn: () => marketService.getMarketTransactions(leagueId),
    enabled: !!leagueId,
  });
};

/**
 * Get buyout clause history
 */
export const useBuyoutHistory = (leagueId: number) => {
  return useQuery({
    queryKey: ['buyout-history', leagueId],
    queryFn: () => marketService.getBuyoutHistory(leagueId),
    enabled: !!leagueId,
  });
};
