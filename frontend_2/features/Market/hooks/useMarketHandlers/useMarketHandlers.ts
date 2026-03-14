import type { DriverWithOwnership } from '@/features/Market/types/marketTypes';
import { useBuyHandlers, type UseBuyHandlersReturn } from './useBuyHandlers';
import { useSellHandlers, type UseSellHandlersReturn } from './useSellHandlers';
import { useListHandlers, type UseListHandlersReturn } from './useListHandlers';

type DialogState = {
    isOpen: boolean;
    type: 'confirm' | 'success' | 'error' | 'info';
    title: string;
    message: string;
    onConfirm?: () => void;
    confirmText?: string;
}

export interface BaseHandlerParams {
    leagueId: number;
    internalUserId: number;
    userBudget: number;
    userDriverCount: number;
    setDialog: (dialog: DialogState) => void;
    dialog: DialogState;
}

export interface UseMarketHandlersParams {
    leagueId: number;
    internalUserId: number;
    freeDrivers?: DriverWithOwnership[];
    forSaleDrivers?: DriverWithOwnership[];
    myDrivers?: DriverWithOwnership[];
    userBudget: number;
    userDriverCount: number;
    buyFromMarket: any;
    buyFromUser: any;
    sellToMarket: any;
    listForSale: any;
    unlistFromSale: any;
    setBuyModalDriver: (driver: DriverWithOwnership | null) => void;
    setSellModalDriver: (driver: DriverWithOwnership | null) => void;
    setListModalDriver: (driver: DriverWithOwnership | null) => void;
    setDialog: (dialog: DialogState) => void;
    dialog: DialogState;
    buyModalDriver: DriverWithOwnership | null;
    sellModalDriver: DriverWithOwnership | null;
    listModalDriver: DriverWithOwnership | null;
}

export interface UseMarketHandlersReturn 
extends UseBuyHandlersReturn, UseListHandlersReturn, UseSellHandlersReturn {

}

export const useMarketHandlers = (
    params: UseMarketHandlersParams
): UseMarketHandlersReturn => {
    const buyHandlers = useBuyHandlers({
        leagueId: params.leagueId,
        internalUserId: params.internalUserId,
        freeDrivers: params.freeDrivers,
        forSaleDrivers: params.forSaleDrivers,
        userBudget: params.userBudget,
        userDriverCount: params.userDriverCount,
        buyFromMarket: params.buyFromMarket,
        buyFromUser: params.buyFromUser,
        setBuyModalDriver: params.setBuyModalDriver,
        buyModalDriver: params.buyModalDriver,
        setDialog: params.setDialog,
        dialog: params.dialog,
    })

    const sellHandlers = useSellHandlers({
        leagueId: params.leagueId,
        internalUserId: params.internalUserId,
        myDrivers: params.myDrivers,
        userBudget: params.userBudget,
        userDriverCount: params.userDriverCount,
        sellToMarket: params.sellToMarket,
        setSellModalDriver: params.setSellModalDriver,
        sellModalDriver: params.sellModalDriver,
        setDialog: params.setDialog,
        dialog: params.dialog,
    })

    const listHandlers = useListHandlers({
        leagueId: params.leagueId,
        internalUserId: params.internalUserId,
        myDrivers: params.myDrivers,
        userBudget: params.userBudget,
        userDriverCount: params.userDriverCount,
        listForSale: params.listForSale,
        unlistFromSale: params.unlistFromSale,
        setListModalDriver: params.setListModalDriver,
        listModalDriver: params.listModalDriver,
        setDialog: params.setDialog,
        dialog: params.dialog,
    })

    return {
        ...buyHandlers,
        ...sellHandlers,
        ...listHandlers,
    };
};
