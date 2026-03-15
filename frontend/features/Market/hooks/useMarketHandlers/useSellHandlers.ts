import type { DriverWithOwnership } from '@/features/Market/types/marketTypes';
import type { BaseHandlerParams } from './useMarketHandlers';

interface UseSellHandlersParams extends BaseHandlerParams {
    myDrivers?: DriverWithOwnership[];
    sellToMarket: any;
    setSellModalDriver: (driver: DriverWithOwnership | null) => void;
    sellModalDriver: DriverWithOwnership | null;
}

export interface UseSellHandlersReturn {
    handleSell: (driverId: number) => void;
    confirmSell: () => void;
}

export const useSellHandlers = ({
    leagueId,
    internalUserId,
    myDrivers,
    sellToMarket,
    setSellModalDriver,
    sellModalDriver,
    setDialog,
}: UseSellHandlersParams): UseSellHandlersReturn => {

    const handleSell = (driverId: number) => {
        const driver = myDrivers?.find(d => d.id === driverId);
        if (driver) {
            setSellModalDriver(driver);
        }
    };

    const confirmSell = () => {
        if (!sellModalDriver || !leagueId) return;

        sellToMarket(
            {
                leagueId,
                driverId: sellModalDriver.id,
                request: {
                    seller_user_id: internalUserId,
                },
            },
            {
                onSuccess: () => {
                    setSellModalDriver(null);
                    setDialog({
                        isOpen: true,
                        type: 'success',
                        title: 'Success!',
                        message: 'Driver sold successfully! 80% refunded to your budget.',
                        confirmText: 'OK',
                    });
                },
                onError: (error: unknown) => {
                    console.error('Error selling driver:', error);
                    const errorMessage = error instanceof Error ? error.message : 'Failed to sell driver';
                    setSellModalDriver(null);
                    setDialog({
                        isOpen: true,
                        type: 'error',
                        title: 'Sale Failed',
                        message: errorMessage,
                        confirmText: 'OK',
                    });
                },
            }
        );
    };

    return {
        handleSell,
        confirmSell,
    }
}
