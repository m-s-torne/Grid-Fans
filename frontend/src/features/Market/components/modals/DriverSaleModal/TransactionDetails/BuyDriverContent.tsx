import { useMarketContext } from '@/core/contexts/MarketContext';
import { useDriverSaleModal } from '@/features/Market/hooks';
import type { DriverWithOwnership } from '@/features/Market/types/marketTypes';
import { formatCurrencyPrecise } from '@/features/Market/utils';

interface BuyDriverContentProps {
  driver: DriverWithOwnership | null;
  price: number;
  userBudget: number;
  budgetAfter: number;
}

export const BuyDriverContent = () => {
  const mode = 'buyDriver'

  const {
    userBudget,
    buyModalDriver: driver
  } = useMarketContext()

  const {
    price,
    budgetAfter
  } = useDriverSaleModal({ driver, mode })

  return (
    <>
      {/* Driver Stats */}
      {(driver!.season_results || driver!.fantasy_stats) && (
        <div className="grid grid-cols-3 gap-2">
          {driver!.season_results && (
            <div className="bg-gray-700/30 rounded-lg p-2 border border-gray-600/50">
              <p className="text-[10px] text-gray-400">Points</p>
              <p className="text-sm font-bold text-white">
                {driver!.season_results.points}
              </p>
            </div>
          )}
          {driver!.fantasy_stats && (
            <>
              <div className="bg-gray-700/30 rounded-lg p-2 border border-gray-600/50">
                <p className="text-[10px] text-gray-400">Avg Finish</p>
                <p className="text-sm font-bold text-white">
                  P{driver!.fantasy_stats.avg_finish?.toLocaleString(undefined, { maximumFractionDigits: 1, useGrouping: false }) || 'N/A'}
                </p>
              </div>
              <div className="bg-gray-700/30 rounded-lg p-2 border border-gray-600/50">
                <p className="text-[10px] text-gray-400">Value</p>
                <p className="text-sm font-bold text-green-400">
                  {formatCurrencyPrecise(price)}
                </p>
              </div>
            </>
          )}
        </div>
      )}

      {/* Budget Impact */}
      <div className="bg-blue-900/20 border border-blue-500/30 rounded-lg p-2.5">
        <h4 className="text-[11px] font-medium text-blue-300 mb-2">Budget Impact</h4>
        <div className="space-y-1.5">
          <div className="flex justify-between items-center">
            <span className="text-gray-400 text-xs">Current Budget:</span>
            <span className="text-white font-bold text-sm">
              {formatCurrencyPrecise(userBudget)}
            </span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-gray-400 text-xs">Driver Cost:</span>
            <span className="text-red-400 font-bold text-sm">
              -{formatCurrencyPrecise(price)}
            </span>
          </div>
          <div className="h-px bg-gray-700 my-1"></div>
          <div className="flex justify-between items-center">
            <span className="text-gray-400 font-medium text-xs">After Purchase:</span>
            <span className={`text-base font-bold ${
              budgetAfter >= 0 ? 'text-green-400' : 'text-red-400'
            }`}>
              {formatCurrencyPrecise(budgetAfter)}
            </span>
          </div>
        </div>
      </div>

      {/* Low budget warning */}
      {budgetAfter < 10_000_000 && budgetAfter >= 0 && (
        <div className="bg-yellow-900/20 border border-yellow-500/30 rounded-lg p-2">
          <div className="flex items-start gap-1.5">
            <svg className="w-4 h-4 text-yellow-400 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            <p className="text-yellow-300 text-[11px]">
              Warning: Your remaining budget will be low. Make sure you have enough for future transactions.
            </p>
          </div>
        </div>
      )}
    </>
  );
};
