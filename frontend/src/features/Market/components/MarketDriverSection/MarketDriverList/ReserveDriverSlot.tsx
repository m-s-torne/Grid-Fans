import { motion } from 'framer-motion';
import { MarketDriverCard, type MarketDriverCardProps } from './MarketDriverCard';
import type { CSSProperties } from 'react';

interface ReserveDriverSlotProps extends MarketDriverCardProps {
  isEmpty?: boolean;
  dragRef?: (element: HTMLElement | null) => void;
  dragStyle?: CSSProperties;
  dragAttributes?: any;
  dragListeners?: any;
  isDragging?: boolean;
  isSwapping?: boolean;
  loading: boolean;
}

export const ReserveDriverSlot = ({
  driver,
  isEmpty = false,
  dragRef,
  dragStyle,
  dragAttributes,
  dragListeners,
  isDragging = false,
  isSwapping = false,
  reserveDriverId,
  userState,
  handlers,
  setExpandedDriver,
  loading= false,
}: ReserveDriverSlotProps) => {

  return (
    <div className="mt-4 sm:mt-6">
      {/* Section Header */}
      <div className="flex items-center gap-2 sm:gap-3 mb-3 sm:mb-4">
        <div className="h-px flex-1 bg-gradient-to-r from-transparent via-gray-600/50 to-transparent"></div>
        <div className="flex items-center gap-1 sm:gap-2 px-2 sm:px-4 py-1.5 sm:py-2 bg-gray-800/50 border border-gray-600/50 rounded-lg">
          <span className="text-gray-300 text-xs sm:text-sm font-semibold whitespace-nowrap">RESERVE DRIVER</span>
        </div>
        <div className="h-px flex-1 bg-gradient-to-r from-transparent via-gray-600/50 to-transparent"></div>
      </div>

      {/* Reserve Slot - Centered and responsive width */}
      <div className="flex justify-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="relative w-full sm:max-w-[50%] lg:max-w-[35%]"
        >
        {isEmpty ? (
          // Empty slot
          <div className="border-2 border-dashed border-gray-600/50 rounded-xl p-4 sm:p-8 bg-gray-800/10 backdrop-blur-sm">
            <div className="text-center">
              <div className="w-12 h-12 sm:w-16 sm:h-16 mx-auto mb-3 sm:mb-4 rounded-full bg-gray-800/30 border-2 border-gray-600/30 flex items-center justify-center">
                <svg
                  className="w-6 h-6 sm:w-8 sm:h-8 text-gray-400/50"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 4v16m8-8H4"
                  />
                </svg>
              </div>
              <h3 className="text-gray-300 font-semibold mb-1 text-sm sm:text-base">Reserve Slot Empty</h3>
              <p className="text-gray-400/60 text-xs sm:text-sm">
                Buy a 4th driver to fill this position
              </p>
            </div>
          </div>
        ) : driver ? (
          // Driver card with neutral border to indicate reserve position
          <div className="relative">
            {isSwapping ? (
              // Show skeleton when swapping
              <div className="p-[2px] bg-gradient-to-r from-blue-500/60 via-blue-600/60 to-blue-500/60 rounded-xl">
                <div className="rounded-xl overflow-hidden">
                  <div className="p-4 rounded-lg bg-gray-800/50 animate-pulse">
                    <div className="flex items-center gap-3 mb-3">
                      <div className="w-12 h-12 rounded-full bg-blue-500/30" />
                      <div className="flex-1">
                        <div className="h-4 bg-blue-500/30 rounded w-3/4 mb-2" />
                        <div className="h-3 bg-blue-500/30 rounded w-1/2" />
                      </div>
                    </div>
                    <div className="grid grid-cols-3 gap-2 mb-3">
                      <div className="h-12 bg-blue-500/20 rounded" />
                      <div className="h-12 bg-blue-500/20 rounded" />
                      <div className="h-12 bg-blue-500/20 rounded" />
                    </div>
                    <div className="h-10 bg-blue-500/20 rounded" />
                    <div className="text-center mt-2 text-xs text-blue-400">
                      Swapping drivers...
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <>
                {/* Neutral gray border wrapper */}
                <div className="p-[2px] bg-gradient-to-r from-gray-600/40 via-gray-500/40 to-gray-600/40 rounded-xl">
                  <div 
                    ref={dragRef}
                    style={{ ...dragStyle, opacity: isDragging ? 0.5 : 1 }}
                    {...dragAttributes}
                    {...dragListeners}
                    className="rounded-xl overflow-hidden touch-none cursor-grab active:cursor-grabbing"
                  >
                    <MarketDriverCard
                      driver={driver}
                      loading={loading}
                      reserveDriverId={reserveDriverId}
                      userState={userState}
                      handlers={handlers}
                      setExpandedDriver={setExpandedDriver}
                    />
                  </div>
                </div>
            
                {/* Drag hint */}
                <div className="mt-3 text-center">
                  <div className="inline-flex items-center gap-2 px-3 py-1.5 bg-gray-800/40 border border-gray-600/30 rounded-lg">
                    <svg className="w-4 h-4 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z" />
                    </svg>
                    <span className="text-gray-300 text-xs font-medium">
                      Drag to swap with main drivers
                    </span>
                  </div>
                </div>
              </>
            )}
          </div>
        ) : null}
        </motion.div>
      </div>
    </div>
  );
};
