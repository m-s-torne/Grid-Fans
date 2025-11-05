import { createContext, useContext, type Dispatch, type ReactNode, type SetStateAction } from 'react'
import { useLeagueDetail } from '@/features/League/hooks';
import { 
    useFreeDrivers, 
    useDriversForSale, 
    useUserDrivers,
    useReserveDriverDragDrop,
    useSortedMyDrivers,
    useFilteredDrivers,
    useMarketHandlers,
} from '@/features/Market/hooks';
import { useUserTeam } from '@/core/hooks/userTeams';
import { useMarketStates } from '@/features/Market/hooks';
import { useParams } from 'react-router-dom';
import type { BuyDriverResponse, BuyFromUserResponse, DriverWithOwnership, ListDriverResponse, SellDriverResponse } from '@/features/Market/types/marketTypes';
import type { ActiveTab, Dialog } from '@/features/Market/hooks/useMarketState';
import type { League } from '@/core/services';
import type { UserTeam } from '@/core/services/userTeamService';
import type { UseMutateFunction } from '@tanstack/react-query';
import { useMarketOpsOrchestrator, type BuyFromMarketMutation, type BuyFromUserMutation, type ListForSaleMutation, type SellToMarketMutation, type UnlistDriverMutation } from '@/features/Market/hooks/useMarketOps';
import type { SensorDescriptor, SensorOptions } from '@dnd-kit/core/dist/sensors/types';
import type { UseMarketHandlersReturn } from '@/features/Market/hooks/useMarketHandlers/useMarketHandlers';
import type { DragEndEvent } from '@dnd-kit/core';

export type SetStateFunction<T> = Dispatch<SetStateAction<T>>

interface MarketStates {
    expandedDriver: DriverWithOwnership | null;
    setExpandedDriver: SetStateFunction<DriverWithOwnership | null>;
    searchQuery: string;
    setSearchQuery: SetStateFunction<string>;
    buyModalDriver: DriverWithOwnership | null;
    setBuyModalDriver: SetStateFunction<DriverWithOwnership | null>;
    sellModalDriver: DriverWithOwnership | null;
    setSellModalDriver: SetStateFunction<DriverWithOwnership | null>;
    listModalDriver: DriverWithOwnership | null;
    setListModalDriver: SetStateFunction<DriverWithOwnership | null>;
    dialog: Dialog;
    setDialog: SetStateFunction<Dialog>;
    activeTab: ActiveTab | null;
    setActiveTab: SetStateFunction<ActiveTab>
    filteredDrivers: DriverWithOwnership[];
}

interface MarketDataFetch {
    leagueId: string | undefined;
    league: League | undefined;
    leagueLoading: boolean;
    leagueError: Error | null;
    freeDrivers: DriverWithOwnership[] | undefined;
    freeDriversLoading: boolean;
    forSaleDrivers: DriverWithOwnership[] | undefined;
    forSaleLoading: boolean;
    userTeam: UserTeam | null | undefined;
    teamLoading: boolean;
    myDrivers: DriverWithOwnership[] | undefined;
    myDriversLoading: boolean;
    sortedMyDrivers: DriverWithOwnership[];
}

type MutateFunction<T, U> = UseMutateFunction<T, Error, U, unknown>

interface MarketMutations {
    buyFromMarket: MutateFunction<BuyDriverResponse, BuyFromMarketMutation>;
    isBuyingFromMarket: boolean;
    buyFromUser: MutateFunction<BuyFromUserResponse, BuyFromUserMutation>;
    sellToMarket: MutateFunction<SellDriverResponse, SellToMarketMutation>;
    isSellingToMarket: boolean;
    listForSale: MutateFunction<ListDriverResponse, ListForSaleMutation>;
    isListing: boolean;
    unlistFromSale: MutateFunction<ListDriverResponse, UnlistDriverMutation>;
}

export type SwappingIds = {
    mainDriver: number;
    reserve: number;
}

interface DragAndDropVariables {
    sensors: SensorDescriptor<SensorOptions>[];
    swappingDriverIds: SwappingIds | null;
    handleDragEnd: (event: DragEndEvent) => Promise<void>;
}

export interface UserState {
    userDriverCount: number;
    userBudget: number;
    internalUserId: number;
}

export interface MarketContext extends MarketDataFetch, MarketMutations, DragAndDropVariables {
    handlers:  UseMarketHandlersReturn;
    state: MarketStates;
    userState: UserState;
}

const MarketContext = createContext<MarketContext | null>(null)

interface MarketProviderProps {
    children: ReactNode
}

export const MarketProvider = ({ children }: MarketProviderProps) => {
    const { leagueId } = useParams<{ leagueId: string }>();
    const state = useMarketStates();

    // Fetch data
    const { league, isLoading: leagueLoading, error: leagueError } = useLeagueDetail(leagueId || '');
    const { data: freeDrivers, isLoading: freeDriversLoading } = useFreeDrivers(Number(leagueId));
    const { data: forSaleDrivers, isLoading: forSaleLoading } = useDriversForSale(Number(leagueId));
    const { data: userTeam, isLoading: teamLoading } = useUserTeam(Number(leagueId));
    
    // Get user's internal ID from team
    const internalUserId = userTeam?.user_id || 0;
    const { data: myDrivers, isLoading: myDriversLoading } = useUserDrivers(
        Number(leagueId),
        internalUserId
    );

    // Calculate user driver count from actual owned drivers
    const userDriverCount = myDrivers?.length || 0;
    const userBudget = userTeam?.budget_remaining || 0;

    // Sort drivers for "My Drivers" tab by their slot position
    const sortedMyDrivers = useSortedMyDrivers({
        myDrivers,
        userTeam,
    });

    // Mutations
    const {
        buyFromMarket,
        isBuyingFromMarket,
        buyFromUser,
        sellToMarket,
        isSellingToMarket,
        listForSale,
        isListing,
        unlistFromSale,
    } = useMarketOpsOrchestrator()

    // Drag & Drop for reserve driver swap
    const { sensors, swappingDriverIds, handleDragEnd } = useReserveDriverDragDrop({
        leagueId: Number(leagueId),
        userId: internalUserId,
        reserveDriverId: userTeam?.reserve_driver_id,
    });

    // Market operation handlers
    const marketHandlers = useMarketHandlers({
        leagueId: Number(leagueId),
        internalUserId,
        freeDrivers,
        forSaleDrivers,
        myDrivers,
        userBudget,
        userDriverCount,
        buyFromMarket,
        buyFromUser,
        sellToMarket,
        listForSale,
        unlistFromSale,
        setBuyModalDriver: state.setBuyModalDriver,
        setSellModalDriver: state.setSellModalDriver,
        setListModalDriver: state.setListModalDriver,
        setDialog: state.setDialog,
        dialog: state.dialog,
        buyModalDriver: state.buyModalDriver,
        sellModalDriver: state.sellModalDriver,
        listModalDriver: state.listModalDriver,
    });

    // Filter drivers by search query
    const filteredDrivers = useFilteredDrivers({
        freeDrivers,
        forSaleDrivers,
        sortedMyDrivers,
        activeTab: state.activeTab,
        searchQuery: state.searchQuery,
    });
    
    const value: MarketContext = {
        leagueId,
        state: {...state, filteredDrivers},
        handlers: {...marketHandlers},
        userState: {
            userDriverCount,
            userBudget,
            internalUserId,
        },
        league, leagueLoading, leagueError,
        freeDrivers, freeDriversLoading,
        forSaleDrivers, forSaleLoading,
        userTeam, teamLoading,
        myDrivers, myDriversLoading,
        buyFromMarket, isBuyingFromMarket,
        buyFromUser,
        sellToMarket, isSellingToMarket,
        listForSale, isListing,
        unlistFromSale,
        sensors, swappingDriverIds, 
        handleDragEnd, sortedMyDrivers
    }

    return (
        <MarketContext.Provider value={value}>
            {children}
        </MarketContext.Provider>
    )
}

export const useMarketContext = () => {
    const context = useContext(MarketContext)
    if (!context) throw new Error('useMarketContext must be used inside the MarketContextProvider')
    return context
}
