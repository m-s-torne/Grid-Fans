import { useNavigate } from 'react-router-dom';
import { AnimatePresence } from 'framer-motion';
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
    const marketContext = useMarketContext()

    // Loading state
    if (marketContext.leagueLoading || marketContext.freeDriversLoading || marketContext.forSaleLoading || marketContext.myDriversLoading || marketContext.teamLoading) {
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
    if (marketContext.leagueError || !marketContext.league) {
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
                <MarketHeader
                    leagueId={marketContext.leagueId} 
                    league={marketContext.league}
                    userBudget={marketContext.userBudget}
                    userDriverCount={marketContext.userDriverCount}
                    navigate={navigate}
                />

                {/* Tabs & Search */}
                <MarketTabs
                    activeTab={marketContext.activeTab}
                    setActiveTab={marketContext.setActiveTab}
                    searchQuery={marketContext.searchQuery}
                    setSearchQuery={marketContext.setSearchQuery}
                    freeDrivers={marketContext.freeDrivers}
                    forSaleDrivers={marketContext.forSaleDrivers}
                    myDrivers={marketContext.myDrivers}
                />

                {/* Driver List Section */}
                <MarketDriverSection />
            </div>

            {/* Expanded Driver Modal */}
            {marketContext.expandedDriver && (
                <AnimatePresence>
                    <DriverCardExpanded
                        key={marketContext.expandedDriver.id}
                        d={marketContext.expandedDriver as any}
                        setExpanded={() => marketContext.setExpandedDriver(null)}
                    />
                </AnimatePresence>
            )}

            {/* Buy Driver Modal */}
            {marketContext.buyModalDriver && (
                <AnimatePresence>
                    <DriverSaleModal
                        mode="buyDriver"
                    />
                </AnimatePresence>
            )}

            {/* Sell Driver Modal */}
            {marketContext.sellModalDriver && (
                <AnimatePresence>
                    <DriverSaleModal
                        mode="quickSell"
                    />
                </AnimatePresence>
            )}
            

            {/* List for Sale Modal */}
            {marketContext.listModalDriver && (
                <AnimatePresence>
                    <DriverSaleModal
                        mode="listForSale"
                    />
                </AnimatePresence>
            )}

            {/* Confirm/Success/Error Dialog */}
            <ConfirmDialog
                isOpen={marketContext.dialog.isOpen}
                onClose={() => marketContext.setDialog({ ...marketContext.dialog, isOpen: false })}
                onConfirm={marketContext.dialog.onConfirm}
                title={marketContext.dialog.title}
                message={marketContext.dialog.message}
                type={marketContext.dialog.type}
                confirmText={marketContext.dialog.confirmText}
            />
        </div>
    );
};

export default Market;
