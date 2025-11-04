import { motion, AnimatePresence } from 'framer-motion';
import { MarketDriverCard } from './MarketDriverCard';
import { DraggableCard } from './DraggableCard';
import { DraggableReserveSlot } from './DraggableReserveSlot';
import type { MarketContext } from '@/core/contexts/MarketContext';

export interface MarketDriverListProps {
  gridColumns?: 2 | 3 | 4;
  enableDragDrop?: boolean;
  marketContext: MarketContext;
}

export const MarketDriverList = ({
  gridColumns = 4 as const,
  enableDragDrop = false,
  marketContext,
}: MarketDriverListProps) => {

  const loading = marketContext.activeTab === 'free' ? marketContext.freeDriversLoading : 
                        marketContext.activeTab === 'for-sale' ? marketContext.forSaleLoading : 
                        marketContext.myDriversLoading

  const getEmptyMessage = () => {
      if (marketContext.searchQuery) return "No drivers match your search";
      
      if (marketContext.activeTab === 'my-drivers') return "You don't own any drivers yet";
      if (marketContext.activeTab === 'free') return "No free agents available";
      return "No drivers for sale available";
  };
  // Loading skeletons
  if (loading) {
    return (
      <div className={`grid gap-3 sm:gap-4 ${
        gridColumns === 4 ? 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4' :
        gridColumns === 3 ? 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-3' :
        'grid-cols-1 sm:grid-cols-2'
      }`}>
        {Array.from({ length: 8 }).map((_, i) => (
          <div
            key={i}
            className="p-3 sm:p-4 rounded-lg border border-gray-700 bg-gray-800/50 animate-pulse"
          >
            <div className="flex items-center gap-2 sm:gap-3 mb-2 sm:mb-3">
              <div className="w-10 h-10 sm:w-12 sm:h-12 rounded-full bg-gray-700 flex-shrink-0" />
              <div className="flex-1 min-w-0">
                <div className="h-3 sm:h-4 bg-gray-700 rounded w-3/4 mb-2" />
                <div className="h-2 sm:h-3 bg-gray-700 rounded w-1/2" />
              </div>
            </div>
            <div className="grid grid-cols-3 gap-1 sm:gap-2 mb-2 sm:mb-3">
              <div className="h-10 sm:h-12 bg-gray-700 rounded" />
              <div className="h-10 sm:h-12 bg-gray-700 rounded" />
              <div className="h-10 sm:h-12 bg-gray-700 rounded" />
            </div>
            <div className="h-8 sm:h-10 bg-gray-700 rounded" />
          </div>
        ))}
      </div>
    );
  }

  // Empty state
  if (marketContext.filteredDrivers.length === 0) {
    return (
      <div className="text-center py-8 sm:py-12">
        <svg
          className="w-12 h-12 sm:w-16 sm:h-16 text-gray-600 mx-auto mb-3 sm:mb-4"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"
          />
        </svg>
        <h3 className="text-gray-400 text-lg sm:text-xl font-semibold mb-2">No Drivers Found</h3>
        <p className="text-gray-500 text-sm sm:text-base">{getEmptyMessage()}</p>
      </div>
    );
  }

  // Driver grid
  // Special layout when drag & drop is enabled (My Drivers tab)
  if (enableDragDrop) {
    const mainDrivers = marketContext.filteredDrivers.filter(d => d.id !== marketContext.userTeam!.reserve_driver_id);
    const reserveDriver = marketContext.filteredDrivers.find(d => d.id === marketContext.userTeam!.reserve_driver_id);

    return (
      <div>
        {/* Main Drivers Section */}
        <div>
          <h3 className="text-gray-300 text-sm sm:text-base font-semibold mb-3 sm:mb-4 flex items-center gap-2">
            <svg className="w-4 h-4 sm:w-5 sm:h-5 text-blue-400 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
              <path fillRule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clipRule="evenodd" />
            </svg>
            Main Lineup
          </h3>
          <div className="grid gap-3 sm:gap-4 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
            <AnimatePresence mode="popLayout">
              {mainDrivers.map((driver) => (
                <motion.div
                  key={driver.id}
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.9 }}
                  transition={{ duration: 0.2 }}
                >
                  <DraggableCard 
                    driver={driver}
                    marketContext={marketContext}
                  />
                </motion.div>
              ))}
            </AnimatePresence>
          </div>
        </div>

        {/* Reserve Driver Section */}
        <DraggableReserveSlot 
          driver={reserveDriver!}
          marketContext={marketContext}
          loading={loading}
        />
      </div>
    );
  }

  // Standard grid layout (for other tabs)
  return (
    <div className={`grid gap-3 sm:gap-4 ${
      gridColumns === 4 ? 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4' :
      gridColumns === 3 ? 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-3' :
      'grid-cols-1 sm:grid-cols-2'
    }`}>
      <AnimatePresence mode="popLayout">
        {marketContext.filteredDrivers.map((driver) => (
          <motion.div
            key={driver.id}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
            transition={{ duration: 0.2 }}
          >
            <MarketDriverCard 
              driver={driver}
              loading={loading}
              userBudget={marketContext.userBudget}
              userDriverCount={marketContext.userDriverCount}
              handleBuyFromMarket={marketContext.handleBuyFromMarket}
              handleBuyFromUser={marketContext.handleBuyFromUser}
              handleSell={marketContext.handleSell}
              handleList={marketContext.handleList}
              handleUnlist={marketContext.handleUnlist}
              handleBuyout={marketContext.handleBuyout}
              setExpandedDriver={marketContext.setExpandedDriver}
              reserveDriverId={marketContext.userTeam!.reserve_driver_id}
              internalUserId={marketContext.internalUserId}
            />
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  );
};
