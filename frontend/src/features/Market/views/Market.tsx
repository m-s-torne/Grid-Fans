import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { 
    DriverCardExpanded, 
    DriverSaleModal,
    MarketHeader,
    MarketTabs,
    MarketDriverSection
} from '@/features/Market/components';
import { ConfirmDialog } from '@/core/components';
import { useMarketContext } from '@/core/contexts/MarketContext';

const Market = () => {
    const navigate = useNavigate();
    const {
        leagueLoading,
        freeDriversLoading,
        forSaleLoading,
        myDriversLoading,
        teamLoading,
        leagueError,
        league,
        setExpandedDriver,
        expandedDriver,
        buyModalDriver,
        setBuyModalDriver,
        confirmSell,
        confirmBuyFromMarket,
        setSellModalDriver,
        confirmList,
        setListModalDriver,
        setDialog,
        dialog,
        isBuyingFromMarket,
        sellModalDriver,
        isSellingToMarket,
        listModalDriver,
        isListing,
    } = useMarketContext()

    // Loading state
    if (leagueLoading || freeDriversLoading || forSaleLoading || myDriversLoading || teamLoading) {
        return (
            <div className="p-4 sm:p-6">
                <div className="max-w-7xl mx-auto">
                    <div className="text-center py-8 sm:py-12">
                        <div className="animate-spin rounded-full h-12 w-12 sm:h-16 sm:w-16 border-b-2 border-red-500 mx-auto mb-4"></div>
                        <p className="text-gray-400 text-base sm:text-lg">
                            Loading market...
                        </p>
                    </div>
                </div>
            </div>
        );
    }

    // Error state
    if (leagueError || !league) {
        return (
            <div className="p-4 sm:p-6">
                <div className="max-w-7xl mx-auto">
                    <div className="text-center py-8 sm:py-12">
                        <svg className="w-12 h-12 sm:w-16 sm:h-16 text-red-500 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <h2 className="text-red-400 text-xl sm:text-2xl font-bold mb-2">Access Denied</h2>
                        <p className="text-gray-400 text-base sm:text-lg mb-4">You are not a member of this league</p>
                        <button
                            onClick={() => navigate('/leagues')}
                            className="bg-gray-600 hover:bg-gray-700 text-white px-4 sm:px-6 py-2 text-sm sm:text-base rounded-lg transition-colors cursor-pointer"
                        >
                            Back to Leagues
                        </button>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="p-4 sm:p-6 lg:p-8">
            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <MarketHeader/>

                {/* Tabs & Search */}
                <MarketTabs/>

                {/* Driver List Section */}
                <MarketDriverSection />
            </div>

            {/* Expanded Driver Modal */}
            <AnimatePresence>
                {expandedDriver && (
                    <div>
                        <DriverCardExpanded
                            key={expandedDriver.id}
                            d={expandedDriver as any}
                            setExpanded={() => setExpandedDriver(null)}
                        />
                    </div>
                )}
            </AnimatePresence>

            {/* Buy Driver Modal */}
            {buyModalDriver && (
                <AnimatePresence>
                    <DriverSaleModal
                        mode="buyDriver"
                    />
                </AnimatePresence>
            )}

            {/* Sell Driver Modal */}
            {sellModalDriver && (
                <AnimatePresence>
                    <DriverSaleModal
                        mode="quickSell"
                    />
                </AnimatePresence>
            )}
            

            {/* List for Sale Modal */}
            {listModalDriver && (
                <AnimatePresence>
                    <DriverSaleModal
                        mode="listForSale"
                    />
                </AnimatePresence>
            )}

            {/* Confirm/Success/Error Dialog */}
            <ConfirmDialog
                isOpen={dialog.isOpen}
                onClose={() => setDialog({ ...dialog, isOpen: false })}
                onConfirm={dialog.onConfirm}
                title={dialog.title}
                message={dialog.message}
                type={dialog.type}
                confirmText={dialog.confirmText}
            />
        </div>
    );
};

export default Market;
