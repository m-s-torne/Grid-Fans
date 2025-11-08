import { motion } from 'framer-motion';
import { OwnershipBadge } from './OwnershipBadge';
import { LockCountdown } from './LockCountdown';
import { PriceDisplay } from './PriceDisplay';
import { useDriverActionButton } from '@/features/Market/hooks';
import { getDriverLastName } from '@/features/Market/utils';
import type { DriverWithOwnership } from '@/features/Market/types/marketTypes';
import type { SetStateFunction, UserState } from '@/core/contexts/MarketContext';
import { useDriverCardLogic } from '@/features/Market/hooks/useDriverCardLogic';
import type { UseMarketHandlersReturn } from '@/features/Market/hooks/useMarketHandlers/useMarketHandlers';

export interface MarketDriverCardProps {
  driver: DriverWithOwnership;
  loading?: boolean;
  reserveDriverId: number | null;
  userState: UserState;
  handlers: UseMarketHandlersReturn;
  setExpandedDriver: SetStateFunction<DriverWithOwnership | null>;
}

export const MarketDriverCard = ({
  driver,
  loading = false,
  reserveDriverId,
  userState,
  handlers,
  setExpandedDriver,
}: MarketDriverCardProps) => {

  const {
    pricing,
    actions,
    ownership,
    isReserve,
    isLocked,
    priceType,
    price,
    showSellMenu,
    setShowSellMenu,
  } = useDriverCardLogic({
    driver,
    ...userState,
    reserveDriverId,
  })

  const { renderActionButton } = useDriverActionButton({
    pricing,
    actions,
    loading,
    driverId: driver.id,
    showSellMenu,
    setShowSellMenu,
    handlers,
  })

  return (
    <motion.div
      key={driver.id}
      className="p-3 sm:p-4 rounded-lg border backdrop-blur-[10px] cursor-default"
      style={{
        borderColor: `${driver.driver_color}60`,
        backgroundColor: `${driver.driver_color}20`,
      }}
      whileHover={{
        borderColor: `${driver.driver_color}`,
        backgroundColor: `${driver.driver_color}30`,
        scale: 1.02,
      }}
      transition={{
        duration: 0.15,
        ease: 'easeOut',
      }}
    >
      {/* Header with photo, name, and badges */}
      <div className="flex items-start gap-2 sm:gap-3 mb-2 sm:mb-3">
        <img
          src={driver.headshot_url}
          alt={driver.full_name}
          className="w-10 h-10 sm:w-12 sm:h-12 rounded-full object-cover object-top flex-shrink-0"
        />
        <div className="flex-1 min-w-0">
          <p className="text-white font-medium truncate text-sm sm:text-base">{getDriverLastName(driver.full_name)}</p>
          <p className="text-gray-100 text-xs sm:text-sm truncate">{driver.team_name}</p>
          <div className="mt-1 flex flex-wrap gap-1">
            <OwnershipBadge
              ownership={ownership}
              currentUserId={userState.internalUserId}
              isReserve={isReserve}
              compact
            />
            {isLocked && ownership?.locked_until && <LockCountdown lockedUntil={ownership.locked_until} compact />}
          </div>
        </div>
        <div
          onClick={(e) => {
            e.stopPropagation();
            setExpandedDriver?.(driver);
          }}
          className="p-1.5 sm:p-2 rounded-lg bg-gray-700/60 hover:bg-gray-500/80 border border-gray-600/40 hover:border-gray-400/60 transition-all duration-150 cursor-pointer group shadow-lg hover:shadow-xl flex-shrink-0"
        >
          <svg
            className="w-4 h-4 sm:w-5 sm:h-5 text-gray-200 group-hover:text-white transition-colors"
            fill="currentColor"
            viewBox="0 0 20 20"
          >
            <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z" />
          </svg>
        </div>
      </div>

      {/* Stats grid */}
      <div className="grid grid-cols-3 gap-1 sm:gap-2 text-xs mb-2 sm:mb-3">
        <div className="text-center p-1.5 sm:p-2 bg-gray-100/30 rounded">
          <p className="text-gray-100 text-[10px] sm:text-xs">Points</p>
          <p className="text-white font-bold text-xs sm:text-sm">{driver.season_results?.points || 0}</p>
        </div>
        <div className="text-center p-1.5 sm:p-2 bg-gray-100/30 rounded">
          <p className="text-gray-100 text-[10px] sm:text-xs">Avg Finish</p>
          <p className="text-white font-bold text-xs sm:text-sm">{driver.fantasy_stats?.avg_finish?.toLocaleString(undefined, { maximumFractionDigits: 1, useGrouping: false }) || 'N/A'}</p>
        </div>
        <PriceDisplay
          price={price}
          type={priceType}
          showIcon={false}
        />
      </div>

      {/* Action button */}
      {renderActionButton()}
    </motion.div>
  );
};
