import { formatCurrencyPrecise } from '@/features/Market/utils';

interface ListForSaleContentProps {
  acquisitionPrice: number;
  inputValue: string;
  error: string | null;
  profit: number;
  profitPercentage: string;
  loading: boolean;
  onPriceChange: (value: string) => void;
  onPresetClick: (multiplier: number) => void;
}

export const ListForSaleContent = ({
  acquisitionPrice,
  inputValue,
  error,
  profit,
  profitPercentage,
  loading,
  onPriceChange,
  onPresetClick
}: ListForSaleContentProps) => {
  return (
    <>
      {/* Acquisition Price */}
      <div className="bg-gray-700/30 rounded-lg p-2 border border-gray-600/50">
        <div className="text-[10px] text-gray-400">Your acquisition price</div>
        <div className="text-base font-bold text-white">
          {formatCurrencyPrecise(acquisitionPrice)}
        </div>
      </div>

      {/* Price Input */}
      <div>
        <label className="block text-[10px] font-medium text-gray-300 mb-1">
          Set asking price
        </label>
        <div className="relative">
          <span className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-sm">
            $
          </span>
          <input
            type="text"
            value={inputValue}
            onChange={(e) => onPriceChange(e.target.value)}
            className="w-full pl-7 pr-10 py-1.5 bg-gray-900 border border-gray-600 rounded-lg text-white text-sm font-medium focus:outline-none focus:border-yellow-500 transition-colors"
            placeholder="0.0"
            disabled={loading}
          />
          <span className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 text-[10px]">
            M
          </span>
        </div>
        {error && (
          <div className="mt-1 text-[10px] text-red-400 flex items-center gap-1">
            ⚠️ {error}
          </div>
        )}
      </div>

      {/* Price Presets */}
      <div className="grid grid-cols-4 gap-1.5">
        <button
          onClick={() => onPresetClick(0.9)}
          disabled={loading}
          className="px-2 py-1 bg-gray-700 hover:bg-gray-600 rounded text-[10px] text-white transition-colors"
        >
          -10%
        </button>
        <button
          onClick={() => onPresetClick(1.05)}
          disabled={loading}
          className="px-2 py-1 bg-gray-700 hover:bg-gray-600 rounded text-[10px] text-white transition-colors"
        >
          +5%
        </button>
        <button
          onClick={() => onPresetClick(1.1)}
          disabled={loading}
          className="px-2 py-1 bg-gray-700 hover:bg-gray-600 rounded text-[10px] text-white transition-colors"
        >
          +10%
        </button>
        <button
          onClick={() => onPresetClick(1.2)}
          disabled={loading}
          className="px-2 py-1 bg-gray-700 hover:bg-gray-600 rounded text-[10px] text-white transition-colors"
        >
          +20%
        </button>
      </div>

      {/* Profit/Loss Indicator */}
      <div className={`rounded-lg p-2 border ${
        profit >= 0
          ? 'bg-green-900/20 border-green-700/50'
          : 'bg-red-900/20 border-red-700/50'
      }`}>
        <div className="flex items-center justify-between">
          <span className="text-[10px] text-gray-300">Expected profit/loss</span>
          <div className="text-right">
            <div className={`text-sm font-bold ${
              profit >= 0 ? 'text-green-400' : 'text-red-400'
            }`}>
              {profit >= 0 ? '+' : ''}{formatCurrencyPrecise(profit)}
            </div>
            <div className={`text-[9px] ${
              profit >= 0 ? 'text-green-500' : 'text-red-500'
            }`}>
              ({profit >= 0 ? '+' : ''}{profitPercentage}%)
            </div>
          </div>
        </div>
      </div>
    </>
  );
};
