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
import type { UseMarketHandlersParams, UseMarketHandlersReturn } from '@/features/Market/hooks/useMarketHandlers/useMarketHandlers';
import type { DragEndEvent } from '@dnd-kit/core';

type SetStateFunction<T> = Dispatch<SetStateAction<T | null>>

interface MarketStates {
    expandedDriver: DriverWithOwnership | null;
    setExpandedDriver: SetStateFunction<DriverWithOwnership>;
    searchQuery: string;
    setSearchQuery: Dispatch<SetStateAction<string>>;
    buyModalDriver: DriverWithOwnership | null;
    setBuyModalDriver: SetStateFunction<DriverWithOwnership>;
    sellModalDriver: DriverWithOwnership | null;
    setSellModalDriver: SetStateFunction<DriverWithOwnership>;
    listModalDriver: DriverWithOwnership | null;
    setListModalDriver: SetStateFunction<DriverWithOwnership>;
    dialog: Dialog;
    setDialog: Dispatch<SetStateAction<Dialog>>;
    sortedMyDrivers: DriverWithOwnership[];
    activeTab: ActiveTab | null;
    setActiveTab: SetStateFunction<ActiveTab | null>
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

interface DragAndDropVariables {
    sensors: SensorDescriptor<SensorOptions>[];
    swappingDriverIds: {
        mainDriver: number;
        reserve: number;
    } | null;
    handleDragEnd: (event: DragEndEvent) => Promise<void>;
}

interface MarketComputedData {
    internalUserId: number;
    userDriverCount: number;
    userBudget: number;
    filteredDrivers: DriverWithOwnership[];
}

export interface MarketContext extends MarketStates, MarketDataFetch, MarketMutations, DragAndDropVariables, MarketComputedData, UseMarketHandlersReturn {
    useMarketHandlers: (params: UseMarketHandlersParams) => UseMarketHandlersReturn;
}

const MarketContext = createContext<MarketContext | null>(null)

interface MarketProviderProps {
    children: ReactNode
}

export const MarketProvider = ({ children }: MarketProviderProps) => {
    const { leagueId } = useParams<{ leagueId: string }>();
    const {
        expandedDriver, setExpandedDriver,
        searchQuery, setSearchQuery,
        activeTab, setActiveTab,
        buyModalDriver, setBuyModalDriver,
        sellModalDriver, setSellModalDriver,
        listModalDriver, setListModalDriver,
        dialog, setDialog
    } = useMarketStates()

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
        setBuyModalDriver,
        setSellModalDriver,
        setListModalDriver,
        setDialog,
        dialog,
        buyModalDriver,
        sellModalDriver,
        listModalDriver,
    });

    // Filter drivers by search query
    const filteredDrivers = useFilteredDrivers({
        freeDrivers,
        forSaleDrivers,
        sortedMyDrivers,
        activeTab,
        searchQuery,
    });
    
    const value: MarketContext = {
        leagueId,
        expandedDriver, setExpandedDriver,
        searchQuery, setSearchQuery,
        activeTab, setActiveTab,
        buyModalDriver, setBuyModalDriver,
        sellModalDriver, setSellModalDriver,
        listModalDriver, setListModalDriver,
        dialog, setDialog,
        ...marketHandlers,
        league, leagueLoading, leagueError,
        freeDrivers, freeDriversLoading,
        forSaleDrivers, forSaleLoading,
        userTeam, teamLoading,
        internalUserId,
        myDrivers, myDriversLoading,
        userDriverCount, userBudget,
        sortedMyDrivers,
        buyFromMarket, isBuyingFromMarket,
        buyFromUser,
        sellToMarket, isSellingToMarket,
        listForSale, isListing,
        unlistFromSale,
        sensors, swappingDriverIds, handleDragEnd,
        useMarketHandlers, filteredDrivers
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
