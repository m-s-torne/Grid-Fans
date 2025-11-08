/**
 * Hook for rendering driver card action buttons
 * This is a TRUE hook - it returns JSX and uses React features
 */
import type { DriverPricing } from '@/features/Market/utils/driverPricing';
import type { DriverCardActions } from '@/features/Market/utils/driverActions';
import { formatCurrencyPrecise } from '@/features/Market/utils/currencyFormat';
import type { UseMarketHandlersReturn } from './useMarketHandlers/useMarketHandlers';

interface UseDriverActionButtonParams {
  pricing: DriverPricing;
  actions: DriverCardActions;
  loading: boolean;
  driverId: number;
  showSellMenu: boolean;
  setShowSellMenu: (show: boolean) => void;
  handlers: UseMarketHandlersReturn;
}

export const useDriverActionButton = ({
  pricing,
  actions,
  loading,
  driverId,
  showSellMenu,
  setShowSellMenu,
  handlers,
}: UseDriverActionButtonParams) => {
  const { refundPrice } = pricing;
  const { actionType, canExecuteAction, canAfford, canAffordBuyout, hasSpace } = actions;

  if (actionType === 'buy-free-agent') {
    console.log(
      !!canExecuteAction
    )
  }

  const renderActionButton = () => {
    switch (actionType) {
      case 'buy-free-agent':
        return (
          <button
            onClick={(e) => {
              e.stopPropagation();
              if (canExecuteAction) handlers.handleBuyFromMarket(driverId);
            }}
            disabled={!canExecuteAction || loading}
            className={`w-full px-3 py-2 rounded-lg font-medium text-sm transition-all ${
              canExecuteAction
                ? 'bg-green-600 hover:bg-green-700 text-white hover:cursor-pointer'
                : 'bg-gray-600 text-gray-400 cursor-not-allowed'
            }`}
          >
            {!hasSpace ? '4/4 Drivers' : !canAfford ? 'Not enough $' : loading ? 'Buying...' : 'Buy'}
          </button>
        );

      case 'locked-by-me':
        return (
          <div className="w-full px-3 py-2 rounded-lg font-medium text-sm bg-gray-700 text-gray-400 text-center cursor-not-allowed flex items-center justify-center gap-1">
            🔒 Locked
          </div>
        );

      case 'unlist':
        return (
          <button
            onClick={(e) => {
              e.stopPropagation();
              handlers.handleUnlist(driverId);
            }}
            disabled={loading}
            className="w-full px-3 py-2 rounded-lg font-medium text-sm bg-gray-600 hover:bg-gray-700 text-white transition-all"
          >
            {loading ? 'Unlisting...' : 'Unlist'}
          </button>
        );

      case 'sell-options':
        return (
          <div className="relative">
            <button
              onClick={(e) => {
                e.stopPropagation();
                setShowSellMenu(!showSellMenu);
              }}
              disabled={loading}
              className="hover:cursor-pointer w-full px-3 py-2 rounded-lg font-medium text-sm bg-blue-600 hover:bg-blue-700 text-white transition-all flex items-center justify-center gap-1"
            >
              Sell Options
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
              </svg>
            </button>

            {showSellMenu && (
              <div className="absolute bottom-full left-0 right-0 mb-1 bg-gray-800 border border-gray-600 rounded-lg shadow-xl z-10 overflow-hidden">
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    setShowSellMenu(false);
                    handlers.handleSell(driverId);
                  }}
                  className="w-full px-3 py-2 text-left text-sm text-white hover:bg-red-600/50 transition-colors flex items-center gap-2"
                >
                  <span>💸</span>
                  <div>
                    <div className="font-medium">Quick Sell</div>
                    <div className="text-xs text-gray-400">80% refund ({formatCurrencyPrecise(refundPrice)})</div>
                  </div>
                </button>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    setShowSellMenu(false);
                    handlers.handleList(driverId);
                  }}
                  className="w-full px-3 py-2 text-left text-sm text-white hover:bg-yellow-600/50 transition-colors flex items-center gap-2 border-t border-gray-700"
                >
                  <span>💰</span>
                  <div>
                    <div className="font-medium">List for Sale</div>
                    <div className="text-xs text-gray-400">Set custom price</div>
                  </div>
                </button>
              </div>
            )}
          </div>
        );

      case 'buy-listed':
        return (
          <button
            onClick={(e) => {
              e.stopPropagation();
              if (canExecuteAction) handlers.handleBuyFromUser(driverId);
            }}
            disabled={!canExecuteAction || loading}
            className={`w-full px-3 py-2 rounded-lg font-medium text-sm transition-all ${
              canExecuteAction
                ? 'bg-yellow-600 hover:bg-yellow-700 text-white'
                : 'bg-gray-600 text-gray-400 cursor-not-allowed'
            }`}
          >
            {!hasSpace ? '4/4 Drivers' : !canAfford ? 'Not enough $' : loading ? 'Buying...' : 'Buy Listed'}
          </button>
        );

      case 'buyout':
        return (
          <button
            onClick={(e) => {
              e.stopPropagation();
              if (canExecuteAction) handlers.handleBuyout(driverId);
            }}
            disabled={!canExecuteAction || loading}
            className={`w-full px-3 py-2 rounded-lg font-medium text-sm transition-all flex items-center justify-center gap-1 ${
              canExecuteAction
                ? 'bg-orange-600 hover:bg-orange-700 text-white'
                : 'bg-gray-600 text-gray-400 cursor-not-allowed'
            }`}
          >
            <span>🔥</span>
            {!hasSpace ? '4/4 Drivers' : !canAffordBuyout ? 'Not enough $' : loading ? 'Buying out...' : 'Buyout'}
          </button>
        );

      case 'locked-by-other':
      default:
        return (
          <div className="w-full px-3 py-2 rounded-lg font-medium text-sm bg-gray-700 text-gray-400 text-center cursor-not-allowed">
            Locked
          </div>
        );
    }
  };

  return { renderActionButton };
};
