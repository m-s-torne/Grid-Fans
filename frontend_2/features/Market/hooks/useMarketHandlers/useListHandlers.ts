import type { DriverWithOwnership } from '@/features/Market/types/marketTypes';
import type { BaseHandlerParams } from './useMarketHandlers';

interface UseListHandlersParams extends BaseHandlerParams {
    myDrivers?: DriverWithOwnership[];
    listForSale: any;
    unlistFromSale: any;
    setListModalDriver: (driver: DriverWithOwnership | null) => void;
    listModalDriver: DriverWithOwnership | null;
}

export interface UseListHandlersReturn {
    handleList: (driverId: number) => void;
    confirmList: (askingPrice: number) => void;
    handleUnlist: (driverId: number) => void;
}

export const useListHandlers = ({
    leagueId,
    internalUserId,
    myDrivers,
    listForSale,
    unlistFromSale,
    setListModalDriver,
    listModalDriver,
    setDialog,
    dialog,
}: UseListHandlersParams): UseListHandlersReturn => {
    
    const handleList = (driverId: number) => {
        const driver = myDrivers?.find(d => d.id === driverId);
        if (driver) {
            setListModalDriver(driver);
        }
    };

    const confirmList = (askingPrice: number) => {
        if (!listModalDriver || !leagueId) return;

        listForSale(
            {
                leagueId,
                driverId: listModalDriver.id,
                request: {
                    owner_user_id: internalUserId,
                    asking_price: askingPrice,
                },
            },
            {
                onSuccess: () => {
                    setListModalDriver(null);
                    setDialog({
                        isOpen: true,
                        type: 'success',
                        title: 'Listed for Sale!',
                        message: 'Your driver is now available in the "For Sale" tab.',
                        confirmText: 'OK',
                    });
                },
                onError: (error: unknown) => {
                    console.error('Error listing driver:', error);
                    const errorMessage = error instanceof Error ? error.message : 'Failed to list driver';
                    setListModalDriver(null);
                    setDialog({
                        isOpen: true,
                        type: 'error',
                        title: 'Listing Failed',
                        message: errorMessage,
                        confirmText: 'OK',
                    });
                },
            }
        );
    };

    const handleUnlist = (driverId: number) => {
        setDialog({
            isOpen: true,
            type: 'confirm',
            title: 'Unlist Driver',
            message: 'Remove this driver from sale listings?',
            confirmText: 'Unlist',
            onConfirm: () => {
                setDialog({ ...dialog, isOpen: false });
                unlistFromSale(
                    {
                        leagueId,
                        driverId: driverId,
                        request: {
                            owner_user_id: internalUserId,
                        },
                    },
                    {
                        onSuccess: () => {
                            setDialog({
                                isOpen: true,
                                type: 'success',
                                title: 'Unlisted!',
                                message: 'Driver removed from sale listings.',
                                confirmText: 'OK',
                            });
                        },
                        onError: (error: unknown) => {
                            console.error('Error unlisting driver:', error);
                            const errorMessage = error instanceof Error ? error.message : 'Failed to unlist driver';
                            setDialog({
                                isOpen: true,
                                type: 'error',
                                title: 'Unlist Failed',
                                message: errorMessage,
                                confirmText: 'OK',
                            });
                        },
                    }
                );
            },
        });
    };

    return {
        handleList,
        confirmList,
        handleUnlist
    }
}
