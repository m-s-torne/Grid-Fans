import type { DriverWithOwnership } from '@/features/Market/types/marketTypes';
import type { BaseHandlerParams } from './useMarketHandlers';
import { formatCurrencyPrecise } from '@/features/Market/utils';

interface UseBuyHandlersParams extends BaseHandlerParams {
    freeDrivers?: DriverWithOwnership[];
    forSaleDrivers?: DriverWithOwnership[];
    buyFromMarket: any;
    buyFromUser: any;
    setBuyModalDriver: (driver: DriverWithOwnership | null) => void;
    buyModalDriver: DriverWithOwnership | null;
}

export interface UseBuyHandlersReturn {
    handleBuyFromMarket: (driverId: number) => void;
    confirmBuyFromMarket: () => void;
    handleBuyFromUser: (driverId: number) => void;
    handleBuyout: (driverId: number) => void;
}

export const useBuyHandlers = ({
    leagueId,
    internalUserId,
    freeDrivers,
    forSaleDrivers,
    userBudget,
    userDriverCount,
    buyFromMarket,
    buyFromUser,
    setBuyModalDriver,
    buyModalDriver,
    setDialog,
    dialog,
}: UseBuyHandlersParams): UseBuyHandlersReturn => {
    const handleBuyFromMarket = (driverId: number) => {
        const driver = freeDrivers?.find(d => d.id === driverId);
        if (driver) {
            setBuyModalDriver(driver);
        }
    };

    const confirmBuyFromMarket = () => {
        if (!buyModalDriver || !leagueId) return;

        buyFromMarket(
            {
                leagueId,
                driverId: buyModalDriver.id,
                request: {
                    buyer_user_id: internalUserId,
                },
            },
            {
                onSuccess: () => {
                    setBuyModalDriver(null);
                    setDialog({
                        isOpen: true,
                        type: 'success',
                        title: 'Success!',
                        message: 'Driver purchased successfully!',
                        confirmText: 'OK',
                    });
                },
                onError: (error: unknown) => {
                    console.error('Error buying driver:', error);
                    const errorMessage = error instanceof Error ? error.message : 'Failed to buy driver';
                    setBuyModalDriver(null);
                    setDialog({
                        isOpen: true,
                        type: 'error',
                        title: 'Purchase Failed',
                        message: errorMessage,
                        confirmText: 'OK',
                    });
                },
            }
        );
    };

    const handleBuyFromUser = (driverId: number) => {
        const driver = forSaleDrivers?.find(d => d.id === driverId);
        if (!driver) return;

        const price = driver.ownership?.asking_price || driver.ownership?.acquisition_price || driver.fantasy_stats?.price || 0;
        const sellerId = driver.ownership?.owner_id;

        if (!sellerId) {
            setDialog({
                isOpen: true,
                type: 'error',
                title: 'Error',
                message: 'Seller information not found',
                confirmText: 'OK',
            });
            return;
        }

        const canAfford = userBudget >= price;
        const hasSpace = userDriverCount < 4;

        if (!hasSpace) {
            setDialog({
                isOpen: true,
                type: 'error',
                title: 'Maximum Drivers Reached',
                message: 'You already have 4 drivers. You cannot buy more until you sell one.',
                confirmText: 'OK',
            });
            return;
        }

        if (!canAfford) {
            setDialog({
                isOpen: true,
                type: 'error',
                title: 'Insufficient Budget',
                message: `You need ${formatCurrencyPrecise(price)} but only have ${formatCurrencyPrecise(userBudget)}`,
                confirmText: 'OK',
            });
            return;
        }

        setDialog({
            isOpen: true,
            type: 'confirm',
            title: 'Buy Driver',
            message: `Buy ${driver.full_name} for ${formatCurrencyPrecise(price)}?`,
            confirmText: 'Buy',
            onConfirm: () => {
                setDialog({ ...dialog, isOpen: false });
                buyFromUser(
                    {
                        leagueId,
                        driverId: driverId,
                        request: {
                            buyer_user_id: internalUserId,
                            seller_user_id: sellerId,
                        },
                    },
                    {
                        onSuccess: () => {
                            setDialog({
                                isOpen: true,
                                type: 'success',
                                title: 'Success!',
                                message: 'Driver purchased successfully!',
                                confirmText: 'OK',
                            });
                        },
                        onError: (error: unknown) => {
                            console.error('Error buying driver:', error);
                            const errorMessage = error instanceof Error ? error.message : 'Failed to buy driver';
                            setDialog({
                                isOpen: true,
                                type: 'error',
                                title: 'Purchase Failed',
                                message: errorMessage,
                                confirmText: 'OK',
                            });
                        },
                    }
                );
            },
        });
    };

    const handleBuyout = (driverId: number) => {
        console.log('Buyout:', driverId);
    };

    return {
        handleBuyFromMarket,
        handleBuyFromUser,
        confirmBuyFromMarket,
        handleBuyout,
    }
}
